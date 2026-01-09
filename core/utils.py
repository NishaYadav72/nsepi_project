from core.models import Center

def get_active_center():
    return Center.objects.filter(is_active=True).first()
