"""Review-first canonical S3 publisher. No credentials or deployment output saved."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, BotoCoreError

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "local" / "python"), str(ROOT / "product-registration" / "backend")]
from poc.config import PocError, load_shared, require_live_aws, validate_aws_identity
from product_registration.rules import RuleBundle

KEY = "rules/product-registration-ja.json"


def publish(client, bucket, account_id, data, *, expected_version=None, initial=False, apply=False):
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    digest = hashlib.sha256(raw).hexdigest()
    RuleBundle(data, "prepublication", digest)
    if bool(initial) == bool(expected_version):
        raise PocError("RULES_PUBLISH_CONDITION", "初回指定または現在のバージョンを一つ指定してください。")
    versioning = client.get_bucket_versioning(Bucket=bucket, ExpectedBucketOwner=account_id)
    block = client.get_public_access_block(Bucket=bucket, ExpectedBucketOwner=account_id)["PublicAccessBlockConfiguration"]
    if versioning.get("Status") != "Enabled" or any(block.get(k) is not True for k in ("BlockPublicAcls", "BlockPublicPolicy", "IgnorePublicAcls", "RestrictPublicBuckets")):
        raise PocError("RULES_BUCKET_UNSAFE", "非公開設定とバージョン管理を確認してください。")
    current = None
    # Missing-object reads can be AccessDenied without ListBucket permission.
    # Initial publication relies solely on S3's conditional create, never a HEAD
    # or GET probe and never a broad ListBucket permission.
    if not initial:
        try:
            current = client.get_object(Bucket=bucket, Key=KEY, ExpectedBucketOwner=account_id)
            current["Body"].close()
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") not in {"NoSuchKey", "404"}:
                raise
    if initial and current is not None or expected_version and (current is None or current.get("VersionId") != expected_version):
        raise PocError("RULES_PUBLISH_CONFLICT", "ルールの版が変更されています。最新の内容を確認してください。")
    result = {"applied": False, "sha256": digest, "previous_version": current.get("VersionId") if current else None, "rules_version": data["version"]}
    if not apply:
        return result
    condition = {"IfMatch": current["ETag"]} if current else {"IfNoneMatch": "*"}
    response = client.put_object(Bucket=bucket, Key=KEY, Body=raw, ContentType="application/json; charset=utf-8", ServerSideEncryption="AES256",
        ChecksumSHA256=base64.b64encode(hashlib.sha256(raw).digest()).decode(), Metadata={"sha256": digest}, ExpectedBucketOwner=account_id, **condition)
    version = response.get("VersionId")
    if not version or version == "null":
        raise PocError("RULES_PUBLISH_UNVERIFIED", "保存後のS3版を確認できません。")
    check = client.get_object(Bucket=bucket, Key=KEY, VersionId=version, ExpectedBucketOwner=account_id)
    try:
        observed = check["Body"].read(262145)
    finally:
        check["Body"].close()
    if hashlib.sha256(observed).hexdigest() != digest:
        raise PocError("RULES_PUBLISH_UNVERIFIED", "保存したルールのハッシュが一致しません。")
    return {**result, "applied": True, "version_id": version}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--profile", default="poc-registration-rules-publisher")
    parser.add_argument("--file", type=Path, default=Path(__file__).with_name("product-registration-ja.json"))
    condition = parser.add_mutually_exclusive_group(required=True)
    condition.add_argument("--initial", action="store_true")
    condition.add_argument("--expected-version")
    parser.add_argument("--apply", action="store_true", help="Publish after review; default performs read-only review")
    args = parser.parse_args()
    try:
        require_live_aws(load_shared()["budget"])
        session = boto3.Session(profile_name=args.profile, region_name="ap-northeast-1")
        validate_aws_identity(session, args.account_id, "poc-registration-rules-publisher")
        data = json.loads(args.file.read_text(encoding="utf-8-sig"))
        client = session.client("s3", config=Config(connect_timeout=5, read_timeout=60, retries={"max_attempts": 0}))
        print(json.dumps(publish(client, args.bucket, args.account_id, data, expected_version=args.expected_version, initial=args.initial, apply=args.apply), ensure_ascii=False))
    except PocError as exc:
        print(json.dumps({"error": exc.code, "message": exc.message}, ensure_ascii=False))
        return 1
    except (ClientError, BotoCoreError, ValueError, OSError, KeyError, TypeError):
        print(json.dumps({"error": "RULES_PUBLISH_FAILED", "message": "ルール公開に失敗しました。認証・条件・通信を確認してください。"}, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
