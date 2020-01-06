#!/bin/sh

docker exec -i $(docker ps -qf "name=sdtc_sql_db")  bash <<'EOF'

#nc_secret=c4271547-da8c-444b-bc60-12ad8909cad5
#wp_secret=9aba9cd7-bdc5-4151-865b-8cb2c57bfa52
#keycloack_auth_url=https://auth.tora.mohamedh.me/auth/realms/master/protocol/openid-connect/auth
#keycloack_token_url=https://auth.tora.mohamedh.me/auth/realms/master/protocol/openid-connect/token
#keycloack_userinfo_url=https://auth.tora.mohamedh.me/auth/realms/master/protocol/openid-connect/userinfo
#keycloack_logout_url=https://auth.tora.mohamedh.me/auth/realms/master/protocol/openid-connect/logout


mysql -u root -p$MYSQL_ROOT_PASSWORD << EOQ

USE $MYSQL_DATABASE_NC; 
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'disable_registration', '');
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'no_prune_user_groups', '');
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'openid_providers', '[]');
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'allow_login_connect', '');
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'auto_create_groups', '');
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'create_disabled_users', '');
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'custom_oauth2_providers', '[]');
INSERT INTO oc_appconfig (appid, configkey, configvalue) VALUES ('sociallogin', 'custom_oidc_providers', '[{"name":"internal_keycloak","title":"keycloak","authorizeUrl":"$keycloack_auth_url","tokenUrl":"$keycloack_token_url","userInfoUrl":"$keycloack_userinfo_url","logoutUrl":"$keycloack_logout_url","clientId":"nc_client","clientSecret":"$nc_secret","scope":"openid","groupsClaim":"","style":"","defaultGroup":""}]');


USE $MYSQL_DATABASE;
INSERT INTO wp_options (option_id, option_name, option_value, autoload) VALUES (NULL, 'openid_connect_generic_settings','a:23:{s:10:"login_type";s:6:"button";s:9:"client_id";s:9:"wp_client";s:13:"client_secret";s:${#wp_secret}:"$wp_secret";s:5:"scope";s:6:"openid";s:14:"endpoint_login";s:${#keycloack_auth_url}:"$keycloack_auth_url";s:17:"endpoint_userinfo";s:${#keycloack_userinfo_url}:"$keycloack_userinfo_url";s:14:"endpoint_token";s:${#keycloack_token_url}:"$keycloack_token_url";s:20:"endpoint_end_session";s:${#keycloack_logout_url}:"$keycloack_logout_url";s:12:"identity_key";s:18:"preferred_username";s:12:"no_sslverify";s:1:"1";s:20:"http_request_timeout";s:1:"5";s:15:"enforce_privacy";s:1:"0";s:22:"alternate_redirect_uri";s:1:"0";s:12:"nickname_key";s:18:"preferred_username";s:12:"email_format";s:0:"";s:18:"displayname_format";s:0:"";s:22:"identify_with_username";s:1:"0";s:16:"state_time_limit";s:0:"";s:19:"link_existing_users";s:1:"0";s:18:"redirect_user_back";s:1:"0";s:18:"redirect_on_logout";s:1:"1";s:14:"enable_logging";s:1:"0";s:9:"log_limit";s:4:"1000";}','');
EOQ


EOF
echo "Openid settings configured in WP and nextcloud :) "