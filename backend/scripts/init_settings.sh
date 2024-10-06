#!/usr/bin/sh
git_root=$(git rev-parse --show-toplevel)
echo SQLALCHEMY_DATABASE_URI:
read -r __sqlalchemy_database_uri__

echo AI_API_KEY:
read -r __ai_api_key__

echo AI_MODEL:
read -r __ai_model__

echo AI_ENDPOINT:
read -r __ai_endpoint__

cat "$git_root/backend/settings.py.example" |
    sed "s/__SERVER_PORT__/8000/g" |
    sed "s/__SQLALCHEMY_DATABASE_URI__/$__sqlalchemy_database_uri__/g" |
    sed "s/__AI_ENDPOINT__/$__ai_endpoint__/g" |
    sed "s/__AI_API_KEY__/$__ai_api_key__/g" |
    sed "s/__AI_MODEL__/$__ai_model__/g" > \
        "$git_root/backend/app/settings.py"
