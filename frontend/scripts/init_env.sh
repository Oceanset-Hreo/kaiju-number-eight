#!/usr/bin/sh
git_root=$(git rev-parse --show-toplevel)

echo mapboxgl access token:
read -r __vite_mapboxgl_access_token__

cat "$git_root/frontend/.env.tmpl" |
    sed "s/__VITE_MAPBOXGL_ACCESS_TOKEN__/$__vite_mapboxgl_access_token__/g" > \
        "$git_root/frontend/.env"
