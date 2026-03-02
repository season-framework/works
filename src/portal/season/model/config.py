import season

class BaseConfig(season.util.stdClass):
    DEFAULT_VALUES = dict()

    def __init__(self, values=dict()):
        default = self.DEFAULT_VALUES
        for key in default:
            _type, val = default[key]
            if key not in values:
                if _type is not None:
                    val = _type(val)
                values[key] = val
            else:
                if _type is not None:
                    values[key] = _type(values[key])
        super(BaseConfig, self).__init__(values)
        
    def __getattr__(self, attr):
        val = super(BaseConfig, self).__getattr__(attr)
        if attr in self.DEFAULT_VALUES:
            _type, _default = self.DEFAULT_VALUES[attr]
            if val is None: val = _default
            if _type is not None: val = _type(val)
        return val

def session_create(wiz, user_id):
    session = wiz.model("portal/season/session")
    
def session_user_id():
    session = wiz.model("portal/season/session")
    return session.get("id")

class Config(BaseConfig):
    # DB category/key 매핑: 이 맵에 있는 키만 DB(system_config)를 우선 조회
    # orm_base, session_create, session_user_id, auth_saml_acs 등은 DB 대상 아님
    DB_KEY_MAP = {
        # site
        'pwa_title': ('site', 'pwa_title'),
        'pwa_start_url': ('site', 'pwa_start_url'),
        'pwa_display': ('site', 'pwa_display'),
        'pwa_background_color': ('site', 'pwa_background_color'),
        'pwa_theme_color': ('site', 'pwa_theme_color'),
        'pwa_orientation': ('site', 'pwa_orientation'),
        'pwa_icon': ('site', 'pwa_icon'),
        'pwa_icon_192': ('site', 'pwa_icon_192'),
        'pwa_icon_512': ('site', 'pwa_icon_512'),
        'site_url': ('site', 'site_url'),
        # smtp
        'smtp_host': ('smtp', 'smtp_host'),
        'smtp_port': ('smtp', 'smtp_port'),
        'smtp_sender': ('smtp', 'smtp_sender'),
        'smtp_password': ('smtp', 'smtp_password'),
        # auth
        'auth_login_uri': ('auth', 'auth_login_uri'),
        'auth_logout_uri': ('auth', 'auth_logout_uri'),
        'auth_baseuri': ('auth', 'auth_baseuri'),
        'auth_saml_use': ('auth', 'auth_saml_use'),
        'auth_saml_entity': ('auth', 'auth_saml_entity'),
        'auth_saml_base_path': ('auth', 'auth_saml_base_path'),
        'auth_saml_error_uri': ('auth', 'auth_saml_error_uri'),
        'saml_mode': ('auth', 'saml_mode'),
    }

    DEFAULT_VALUES = {
        # database config
        'orm_base': (str, "db/"),

        # site config
        'site_url': (str, ""),
        
        # pwa config
        'pwa_title': (str, "WIZ Project"),
        'pwa_start_url': (str, "/"),
        'pwa_display': (str, "standalone"),
        'pwa_background_color': (str, "#6C8DF6"),
        'pwa_theme_color': (str, "#6C8DF6"),
        'pwa_orientation': (str, "any"),
        'pwa_icon': (str, "/assets/portal/season/brand/icon.ico"),
        'pwa_icon_192': (str, "/assets/portal/season/brand/icon-192.png"),
        'pwa_icon_512': (str, "/assets/portal/season/brand/icon-512.png"),

        # smtp config
        'smtp_host': (None, None),
        'smtp_port': (int, 587),
        'smtp_sender': (None, None),
        'smtp_password': (None, None),

        # session config
        'session_create': (None, session_create),
        'session_user_id': (None, session_user_id),

        # auth config
        'auth_login_uri': (None, None),
        'auth_logout_uri': (None, None),
        'auth_baseuri': (str, '/auth'),
        'auth_saml_use': (bool, False),
        'auth_saml_entity': (str, 'season'),
        'auth_saml_base_path': (str, 'config/auth/saml'),
        'auth_saml_acs': (None, None),
        'auth_saml_error_uri': (str, '/'),
        'saml_mode': (str, 'config'),
    }

    def __getattr__(self, attr):
        """DB(system_config) 우선 조회, 없으면 season.py fallback.
        dict.get()으로 직접 조회하여 stdClass.__getattr__ → self.get() 재귀 방지."""
        if attr in Config.DB_KEY_MAP:
            category, key_name = Config.DB_KEY_MAP[attr]
            # season.py 기본값 (dict에서 직접 조회하여 재귀 방지)
            file_val = dict.get(self, attr)
            if attr in Config.DEFAULT_VALUES:
                _type, _default = Config.DEFAULT_VALUES[attr]
                if file_val is None:
                    file_val = _default
                if _type is not None and file_val is not None:
                    file_val = _type(file_val)
            try:
                sys_config = wiz.model("portal/season/system_config")
                db_val = sys_config.get(category, key_name)
                if db_val is not None:
                    if attr in Config.DEFAULT_VALUES:
                        _type, _ = Config.DEFAULT_VALUES[attr]
                        if _type is not None:
                            db_val = _type(db_val)
                    return db_val
            except:
                pass
            return file_val
        # Non-DB_KEY_MAP: dict에서 직접 조회 + DEFAULT_VALUES 적용 (재귀 방지)
        val = dict.get(self, attr)
        if attr in self.DEFAULT_VALUES:
            _type, _default = self.DEFAULT_VALUES[attr]
            if val is None:
                val = _default
            if _type is not None and val is not None:
                val = _type(val)
        return val

    def __getitem__(self, key):
        """dict 스타일 접근도 DB 조회 경유."""
        return self.__getattr__(key)

    def get(self, key, default=None):
        """get() 호출도 DB 조회 경유. dict.get 대신 __getattr__로 DB fallback 적용."""
        try:
            val = self.__getattr__(key)
            if val is None:
                return default
            return val
        except:
            return default

config = wiz.config("season")
Model = Config(config)
