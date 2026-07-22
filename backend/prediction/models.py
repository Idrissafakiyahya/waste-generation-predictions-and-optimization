from django.db import models


class Shehia(models.Model):
    """Shehia (administrative division) model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Shehias"

    def __str__(self):
        return self.name


class Bin(models.Model):
    """Waste Bin model"""
    shehia = models.ForeignKey(Shehia, on_delete=models.CASCADE, related_name='bins')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(default=100, help_text="Capacity in kg")
    bin_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Waste'),
            ('organic', 'Organic Waste'),
            ('recyclable', 'Recyclable'),
            ('hazardous', 'Hazardous'),
        ],
        default='general'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['shehia', 'name']
        unique_together = ('shehia', 'name')

    def __str__(self):
        return f"{self.name} ({self.shehia})"


class WasteReport(models.Model):
    """Community waste report model"""
    shehia = models.ForeignKey(Shehia, on_delete=models.CASCADE, related_name='reports')
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='reports')
    timestamp = models.DateTimeField()
    WASTE_LEVEL_CHOICES = [
        ('unknown', 'Unknown'),
        ('low', 'Low (25%)'),
        ('medium', 'Medium (50%)'),
        ('high', 'High (75%)'),
        ('full', 'Full (100%)'),
    ]
    waste_level = models.CharField(max_length=20, choices=WASTE_LEVEL_CHOICES, default='unknown')
    comment = models.TextField('Description', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Report: {self.shehia} - {self.bin} ({self.timestamp})"


class SavedPredictionBatch(models.Model):
    """Batch of saved prediction results."""
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name or self.created_at.strftime('%Y-%m-%d %H:%M:%S')


class SavedPredictionItem(models.Model):
    """Single prediction row saved in a batch."""
    batch = models.ForeignKey(SavedPredictionBatch, on_delete=models.CASCADE, related_name='items')
    shehia = models.CharField(max_length=100)
    bin = models.CharField(max_length=100)
    day_label = models.CharField(max_length=50)
    date = models.DateField()
    formatted_date = models.CharField(max_length=64)
    prediction = models.CharField(max_length=50)
    probabilities = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['batch', 'shehia', 'bin', 'date']

    def __str__(self):
        return f"{self.batch} - {self.shehia}/{self.bin} ({self.day_label})"


class CollectionRecord(models.Model):
    """Record of a bin collection event."""
    shehia = models.ForeignKey(Shehia, on_delete=models.CASCADE, related_name='collection_records')
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='collection_records')
    collected_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('collected', 'Collected'), ('failed', 'Failed')],
        default='collected',
    )
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-collected_at', 'shehia', 'bin']

    def __str__(self):
        return f"{self.bin} collected at {self.collected_at.strftime('%Y-%m-%d %H:%M')}"
