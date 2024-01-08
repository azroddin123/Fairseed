from django_seed import Seed
from accounts.models import UserRole
from .choices import RoleChoices  # If your choices are defined in a separate file

seeder = Seed.seeder()

initial_roles = [
    {'role_name': RoleChoices.ADMIN},
    {'role_name': RoleChoices.CAMPAIGN_APPROVER},
    {'role_name' : RoleChoices.CAMPAIGN_MANAGER},
    {'role_name' : RoleChoices.NORMAL}
    # Add other roles as needed
]

for role_data in initial_roles:
    seeder.add_entity(UserRole, 1, role_data)

seeder.execute()