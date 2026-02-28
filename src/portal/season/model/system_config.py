import datetime

orm = wiz.model("portal/season/orm")
db = orm.use("system_config")

class SystemConfig:
    """DB 기반 설정 관리자. 캐시 + Fallback 패턴."""

    _cache = {}
    _cache_time = None
    CACHE_TTL = 60  # 초

    @staticmethod
    def _refresh_cache():
        now = datetime.datetime.now().timestamp()
        if SystemConfig._cache_time and (now - SystemConfig._cache_time) < SystemConfig.CACHE_TTL:
            return
        try:
            rows = db.rows()
        except:
            SystemConfig._cache = {}
            SystemConfig._cache_time = now
            return
        SystemConfig._cache = {}
        for row in rows:
            cat = row['category']
            key = row['key_name']
            if cat not in SystemConfig._cache:
                SystemConfig._cache[cat] = {}
            SystemConfig._cache[cat][key] = {
                'value': SystemConfig._cast(row['value'], row['value_type']),
                'type': row['value_type'],
                'description': row.get('description', '')
            }
        SystemConfig._cache_time = now

    @staticmethod
    def _cast(value, value_type):
        if value is None:
            return None
        if value_type == 'int':
            try:
                return int(value)
            except:
                return 0
        if value_type == 'bool':
            return str(value).lower() in ('true', '1', 'yes')
        if value_type == 'json':
            import json
            try:
                return json.loads(value)
            except:
                return value
        return value  # string, password

    @staticmethod
    def get(category, key, default=None):
        """DB에서 설정값 조회. 없으면 default 반환."""
        SystemConfig._refresh_cache()
        cat = SystemConfig._cache.get(category, {})
        item = cat.get(key)
        if item is not None:
            return item['value']
        return default

    @staticmethod
    def set(category, key, value, value_type='string', description=None):
        """DB에 설정값 저장."""
        existing = db.get(category=category, key_name=key)
        data = {
            'category': category,
            'key_name': key,
            'value': str(value) if value is not None else None,
            'value_type': value_type,
            'updated': datetime.datetime.now()
        }
        if description is not None:
            data['description'] = description
        if existing:
            db.update(data, category=category, key_name=key)
        else:
            db.insert(data)
        SystemConfig._cache_time = None  # 캐시 무효화

    @staticmethod
    def list(category=None):
        """설정 목록 조회. category 지정 시 해당 카테고리만."""
        kwargs = {}
        if category:
            kwargs['category'] = category
        try:
            rows = db.rows(**kwargs)
        except:
            return []
        for row in rows:
            row['value'] = SystemConfig._cast(row['value'], row['value_type'])
            if row['value_type'] == 'password':
                row['value'] = '********'  # 마스킹
        return rows

    @staticmethod
    def delete(category, key):
        """DB에서 설정 삭제."""
        db.delete(category=category, key_name=key)
        SystemConfig._cache_time = None  # 캐시 무효화

Model = SystemConfig
