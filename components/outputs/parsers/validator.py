class OutputValidator():
    def ends_with_question_mark(cls, field):
        if not field.endswith('?'):
            raise ValueError("Badly formed question!")
        return field

    def is_positive(cls, field):
        if field <= 0:
            raise ValueError("Value must be positive!")
        return field

    def is_non_empty_string(cls, field):
        if not field or not isinstance(field, str):
            raise ValueError("Field must be a non-empty string!")
        return field

    def is_email(cls, field):
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, field):
            raise ValueError("Invalid email address!")
        return field

    def is_in_range(cls, field, min_value, max_value):
        if not (min_value <= field <= max_value):
            raise ValueError(f"Value must be between {min_value} and {max_value}!")
        return field

    def is_alphanumeric(cls, field):
        if not field.isalnum():
            raise ValueError("Field must be alphanumeric!")
        return field

    def has_min_length(cls, field, min_length):
        if len(field) < min_length:
            raise ValueError(f"Field must be at least {min_length} characters long!")
        return field

    def has_max_length(cls, field, max_length):
        if len(field) > max_length:
            raise ValueError(f"Field must be no more than {max_length} characters long!")
        return field

    def is_valid_url(cls, field):
        import re
        url_regex = r'^(http|https)://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(url_regex, field):
            raise ValueError("Invalid URL!")
        return field

    def is_date(cls, field):
        from datetime import datetime
        try:
            datetime.strptime(field, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format! Use YYYY-MM-DD.")
        return field

    def is_time(cls, field):
        from datetime import datetime
        try:
            datetime.strptime(field, '%H:%M:%S')
        except ValueError:
            raise ValueError("Invalid time format! Use HH:MM:SS.")
        return field

    def is_datetime(cls, field):
        from datetime import datetime
        try:
            datetime.strptime(field, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid datetime format! Use YYYY-MM-DD HH:MM:SS.")
        return field

    def is_boolean(cls, field):
        if not isinstance(field, bool):
            raise ValueError("Field must be a boolean!")
        return field

    def is_integer(cls, field):
        if not isinstance(field, int):
            raise ValueError("Field must be an integer!")
        return field

    def is_float(cls, field):
        if not isinstance(field, float):
            raise ValueError("Field must be a float!")
        return field

    def is_list(cls, field):
        if not isinstance(field, list):
            raise ValueError("Field must be a list!")
        return field

    def is_dict(cls, field):
        if not isinstance(field, dict):
            raise ValueError("Field must be a dictionary!")
        return field

    def is_non_empty_list(cls, field):
        if not isinstance(field, list) or not field:
            raise ValueError("Field must be a non-empty list!")
        return field

    def is_non_empty_dict(cls, field):
        if not isinstance(field, dict) or not field:
            raise ValueError("Field must be a non-empty dictionary!")
        return field

    def is_valid_json(cls, field):
        import json
        try:
            json.loads(field)
        except ValueError:
            raise ValueError("Field must be a valid JSON string!")
        return field

    def is_valid_xml(cls, field):
        import xml.etree.ElementTree as ET
        try:
            ET.fromstring(field)
        except ET.ParseError:
            raise ValueError("Field must be a valid XML string!")
        return field

    def is_valid_yaml(cls, field):
        import yaml
        try:
            yaml.safe_load(field)
        except yaml.YAMLError:
            raise ValueError("Field must be a valid YAML string!")
        return field

    def is_valid_ip(cls, field):
        import ipaddress
        try:
            ipaddress.ip_address(field)
        except ValueError:
            raise ValueError("Field must be a valid IP address!")
        return field

    def is_valid_ipv4(cls, field):
        import ipaddress
        try:
            ipaddress.IPv4Address(field)
        except ValueError:
            raise ValueError("Field must be a valid IPv4 address!")
        return field

    def is_valid_ipv6(cls, field):
        import ipaddress
        try:
            ipaddress.IPv6Address(field)
        except ValueError:
            raise ValueError("Field must be a valid IPv6 address!")
        return field

    def is_valid_mac(cls, field):
        import re
        mac_regex = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(mac_regex, field):
            raise ValueError("Field must be a valid MAC address!")
        return field

    def is_valid_credit_card(cls, field):
        import re
        cc_regex = r'^[0-9]{16}$'
        if not re.match(cc_regex, field):
            raise ValueError("Field must be a valid credit card number!")
        return field

    def is_valid_ssn(cls, field):
        import re
        ssn_regex = r'^\d{3}-\d{2}-\d{4}$'
        if not re.match(ssn_regex, field):
            raise ValueError("Field must be a valid SSN!")
        return field

    def is_valid_phone_number(cls, field):
        import re
        phone_regex = r'^\+?1?\d{9,15}$'
        if not re.match(phone_regex, field):
            raise ValueError("Field must be a valid phone number!")
        return field

    def is_valid_zip_code(cls, field):
        import re
        zip_regex = r'^\d{5}(?:[-\s]\d{4})?$'
        if not re.match(zip_regex, field):
            raise ValueError("Field must be a valid ZIP code!")
        return field

    def is_valid_country_code(cls, field):
        import pycountry
        if not pycountry.countries.get(alpha_2=field):
            raise ValueError("Field must be a valid country code!")
        return field

    def is_valid_currency_code(cls, field):
        import pycountry
        if not pycountry.currencies.get(alpha_3=field):
            raise ValueError("Field must be a valid currency code!")
        return field

    def is_valid_language_code(cls, field):
        import pycountry
        if not pycountry.languages.get(alpha_2=field):
            raise ValueError("Field must be a valid language code!")
        return field

    def is_valid_timezone(cls, field):
        import pytz
        if field not in pytz.all_timezones:
            raise ValueError("Field must be a valid timezone!")
        return field

    def is_valid_uuid(cls, field):
        import uuid
        try:
            uuid.UUID(field)
        except ValueError:
            raise ValueError("Field must be a valid UUID!")
        return field

    def is_valid_hex_color(cls, field):
        import re
        hex_color_regex = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
        if not re.match(hex_color_regex, field):
            raise ValueError("Field must be a valid hex color code!")
        return field

    def is_valid_base64(cls, field):
        import base64
        try:
            base64.b64decode(field)
        except Exception:
            raise ValueError("Field must be a valid base64 string!")
        return field

    def is_valid_sha256(cls, field):
        import re
        sha256_regex = r'^[A-Fa-f0-9]{64}$'
        if not re.match(sha256_regex, field):
            raise ValueError("Field must be a valid SHA-256 hash!")
        return field

    def is_valid_md5(cls, field):
        import re
        md5_regex = r'^[A-Fa-f0-9]{32}$'
        if not re.match(md5_regex, field):
            raise ValueError("Field must be a valid MD5 hash!")
        return field

    def is_valid_isbn(cls, field):
        import re
        isbn_regex = r'^(97(8|9))?\d{9}(\d|X)$'
        if not re.match(isbn_regex, field):
            raise ValueError("Field must be a valid ISBN!")
        return field

    def is_valid_credit_card_expiry(cls, field):
        import re
        expiry_regex = r'^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$'
        if not re.match(expiry_regex, field):
            raise ValueError("Field must be a valid credit card expiry date!")
        return field

    def is_valid_cvv(cls, field):
        import re
        cvv_regex = r'^[0-9]{3,4}$'
        if not re.match(cvv_regex, field):
            raise ValueError("Field must be a valid CVV!")
        return field

    def is_valid_license_plate(cls, field):
        import re
        license_plate_regex = r'^[A-Z0-9]{1,7}$'
        if not re.match(license_plate_regex, field):
            raise ValueError("Field must be a valid license plate!")
        return field

    def is_valid_passport_number(cls, field):
        import re
        passport_regex = r'^[A-Z0-9]{5,9}$'
        if not re.match(passport_regex, field):
            raise ValueError("Field must be a valid passport number!")
        return field

    def is_valid_ssn(cls, field):
        import re
        ssn_regex = r'^\d{3}-\d{2}-\d{4}$'
        if not re.match(ssn_regex, field):
            raise ValueError("Field must be a valid SSN!")
        return field