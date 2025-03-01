#! /bin/sh

flask --app frontend_service run -p 6000 --host 0.0.0.0 --debug

flask --app admin_backend_service run -p 5000 --host 0.0.0.0 --debug