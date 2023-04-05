from django.conf import settings
from django.db import models

import sys
if sys.version_info[0] == 3:
    try:
        from django.utils.encoding import smart_str as smart_unicode
    except ImportError:
        from django.utils.encoding import smart_text as smart_unicode
else:
    from django.utils.encoding import smart_unicode

import bleach
from sanitizer.utils import is_bleach_version_5

if is_bleach_version_5():
    from bleach.css_sanitizer import CSSSanitizer


class SanitizedCharField(models.CharField):
    
    def __init__(self, allowed_tags=[], allowed_attributes=[],
                 allowed_styles=[], strip=False, 
                 *args, **kwargs):
        self._sanitizer_allowed_tags = allowed_tags
        self._sanitizer_allowed_attributes = allowed_attributes
        self._sanitizer_allowed_styles = allowed_styles
        self._sanitizer_strip = strip
        super(SanitizedCharField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(SanitizedCharField, self).to_python(value)
        if is_bleach_version_5():
            css_sanitizer = CSSSanitizer(allowed_css_properties=self._sanitizer_allowed_styles)
            value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
                attributes=self._sanitizer_allowed_attributes, 
                css_sanitizer=css_sanitizer, strip=self._sanitizer_strip)
        else:
            value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
                attributes=self._sanitizer_allowed_attributes, 
                styles=self._sanitizer_allowed_styles, strip=self._sanitizer_strip)


class SanitizedTextField(models.TextField):
    
    def __init__(self, allowed_tags=[], allowed_attributes=[], 
                 allowed_styles=[], strip=False, 
                 *args, **kwargs):
        self._sanitizer_allowed_tags = allowed_tags
        self._sanitizer_allowed_attributes = allowed_attributes
        self._sanitizer_allowed_styles = allowed_styles
        self._sanitizer_strip = strip
        super(SanitizedTextField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(SanitizedTextField, self).to_python(value)
        if is_bleach_version_5():
            css_sanitizer = CSSSanitizer(allowed_css_properties=self._sanitizer_allowed_styles)
            value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
                attributes=self._sanitizer_allowed_attributes, 
                css_sanitizer=css_sanitizer, strip=self._sanitizer_strip)
        else:
            value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
                attributes=self._sanitizer_allowed_attributes, 
                styles=self._sanitizer_allowed_styles, strip=self._sanitizer_strip)

    def get_prep_value(self, value):
        value = super(SanitizedTextField, self).get_prep_value(value)
        if is_bleach_version_5():
            css_sanitizer = CSSSanitizer(allowed_css_properties=self._sanitizer_allowed_styles)
            value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
                attributes=self._sanitizer_allowed_attributes, 
                css_sanitizer=css_sanitizer, strip=self._sanitizer_strip)
        else:
            value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
                attributes=self._sanitizer_allowed_attributes, 
                styles=self._sanitizer_allowed_styles, strip=self._sanitizer_strip)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^sanitizer\.models\.SanitizedCharField"])
    add_introspection_rules([], ["^sanitizer\.models\.SanitizedTextField"])
