from django.db import models

class Node(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Edge(models.Model):
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')

    def __str__(self):
        return f"{self.from_node} → {self.to_node}"

class SiteSettings(models.Model):
    service_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f"Service: {'Enabled' if self.service_enabled else 'Disabled'}"