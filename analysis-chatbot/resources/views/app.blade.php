<!doctype html>
<html lang="{{ request()->is('products/new') ? 'ja' : 'ko' }}">
<head>
    <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <meta name="color-scheme" content="light">
    <title>{{ request()->is('products/new') ? '商品登録 · 商品ワークスペース' : '분석 대화 · 데이터에서 답을 찾다' }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.ts'])
</head>
<body><div id="app"></div></body>
</html>
