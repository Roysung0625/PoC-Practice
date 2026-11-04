<?php
return ['url' => env('PYTHON_API_URL', 'http://127.0.0.1:8001'),
    'env_file' => dirname(base_path()).'/.local/app.env', 'token' => null,
    'artifact_directory' => dirname(base_path()).'/.local/analysis-chatbot/artifacts'];
