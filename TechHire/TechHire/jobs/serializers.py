from rest_framework import serializers
from .models import JobPosting

LOCKED = "🔒 Premium Feature"


class JobPostingSerializer(serializers.ModelSerializer):
    """
    Serializer that applies field-level masking for non-premium users.

    Rules:
    - title, description, location, created_at → always visible
    - company_name, salary_range, application_link → visible only when
      the request carries a valid JWT belonging to a Premium member.
    """

    company_name = serializers.SerializerMethodField()
    salary_range = serializers.SerializerMethodField()
    application_link = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = [
            'id',
            'title',
            'description',
            'location',
            'company_name',
            'salary_range',
            'application_link',
            'created_at',
        ]

    # ── Helper ────────────────────────────────────────────────────────────────
    def _is_premium_user(self) -> bool:
        """
        Returns True only when:
          1. A request object exists in the serializer context.
          2. The request user is authenticated (valid JWT).
          3. The user has a UserProfile with membership_tier == 'premium'.
        """
        request = self.context.get('request')
        if not request:
            return False
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, 'userprofile', None)
        if not profile:
            return False
        return profile.is_premium

    # ── Field-level methods ───────────────────────────────────────────────────
    def get_company_name(self, obj):
        return obj.company_name if self._is_premium_user() else LOCKED

    def get_salary_range(self, obj):
        return obj.salary_range if self._is_premium_user() else LOCKED

    def get_application_link(self, obj):
        return obj.application_link if self._is_premium_user() else LOCKED
