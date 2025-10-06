from django.db import models
from django.utils import timezone

class ScrapingSession(models.Model):
    """Model to store scraping sessions and results"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('blocked', 'Blocked'),
    ]
    
    session_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    
    # Scraping results
    forms_count = models.IntegerField(default=0)
    inputs_count = models.IntegerField(default=0)
    selects_count = models.IntegerField(default=0)
    links_count = models.IntegerField(default=0)
    scripts_count = models.IntegerField(default=0)
    
    # Raw data
    raw_html = models.TextField(blank=True)
    parsed_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.session_id} - {self.status}"

class CourtRecord(models.Model):
    """Model to store individual court records"""
    
    session = models.ForeignKey(ScrapingSession, on_delete=models.CASCADE, related_name='records')
    record_type = models.CharField(max_length=100, blank=True)
    case_number = models.CharField(max_length=100, blank=True)
    party_name = models.CharField(max_length=200, blank=True)
    filing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=True)
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.record_type} - {self.party_name}"