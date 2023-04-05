from django import forms

import bleach
from sanitizer.utils import is_bleach_version_5

if is_bleach_version_5():
    from bleach.css_sanitizer import CSSSanitizer


class SanitizedCharField(forms.CharField):
    """
    A subclass of CharField that escapes (or strip) HTML tags and attributes.
    """    
    def __init__(self, allowed_tags=[], allowed_attributes=[], 
            allowed_styles=[], strip=False, *args, **kwargs):
        self._allowed_tags = allowed_tags
        self._allowed_attributes = allowed_attributes
        self._allowed_styles = allowed_styles
        self._strip = strip
        super(SanitizedCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(SanitizedCharField, self).clean(value)
        if is_bleach_version_5():
            css_sanitizer = CSSSanitizer(allowed_css_properties=self._allowed_styles)
            return bleach.clean(value, tags=self._allowed_tags,
                attributes=self._allowed_attributes, 
                css_sanitizer=css_sanitizer, strip=self._strip)
        else:
            return bleach.clean(value, tags=self._allowed_tags,
                attributes=self._allowed_attributes, 
                styles=self._allowed_styles, strip=self._strip)