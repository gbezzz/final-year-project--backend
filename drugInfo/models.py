from django.db import models


class OrthodoxDrug(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cas_number = models.CharField(
        max_length=255, null=True, blank=True, db_column="cas-number"
    )

    state = models.CharField(max_length=50, null=True, blank=True)
    groups = models.CharField(max_length=255, null=True, blank=True)
    general_references = models.TextField(null=True, blank=True)
    synthesis_reference = models.TextField(null=True, blank=True)
    indication = models.TextField(null=True, blank=True)
    pharmacodynamics = models.TextField(null=True, blank=True)
    mechanism_of_action = models.TextField(null=True, blank=True)
    toxicity = models.TextField(null=True, blank=True)
    metabolism = models.TextField(null=True, blank=True)
    absorption = models.TextField(null=True, blank=True)
    half_life = models.CharField(max_length=50, null=True, blank=True)
    protein_binding = models.CharField(max_length=50, null=True, blank=True)
    route_of_elimination = models.TextField(null=True, blank=True)
    volume_of_distribution = models.CharField(max_length=50, null=True, blank=True)
    clearance = models.CharField(max_length=50, null=True, blank=True)
    classification_description = models.TextField(null=True, blank=True)
    direct_parent = models.CharField(max_length=255, null=True, blank=True)
    kingdom = models.CharField(max_length=255, null=True, blank=True)
    superclass = models.CharField(max_length=255, null=True, blank=True)
    drug_class = models.CharField(max_length=255, null=True, blank=True)
    subclass = models.CharField(max_length=255, null=True, blank=True)
    salts = models.TextField(null=True, blank=True)
    synonyms = models.TextField(null=True, blank=True)
    products = models.TextField(null=True, blank=True)
    international_brands = models.TextField(null=True, blank=True)
    mixtures = models.TextField(null=True, blank=True)
    packagers = models.TextField(null=True, blank=True)
    manufacturers = models.TextField(null=True, blank=True)
    prices = models.TextField(null=True, blank=True)
    categories = models.TextField(null=True, blank=True)
    affected_organisms = models.TextField(null=True, blank=True)
    dosages = models.TextField(null=True, blank=True)
    atc_codes = models.TextField(null=True, blank=True)
    ahfs_codes = models.TextField(null=True, blank=True)
    pdb_entries = models.TextField(null=True, blank=True)
    patents = models.TextField(null=True, blank=True)
    food_interactions = models.TextField(null=True, blank=True)
    drug_interactions = models.TextField(null=True, blank=True)
    sequences = models.TextField(null=True, blank=True)
    experimental_properties = models.TextField(null=True, blank=True)
    external_identifiers = models.TextField(null=True, blank=True)
    external_links = models.TextField(null=True, blank=True)
    pathways = models.TextField(null=True, blank=True)
    reactions = models.TextField(null=True, blank=True)
    snp_effects = models.TextField(null=True, blank=True)
    snp_adverse_effects = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "OrthodoxDrug"
        app_label = "drugInfo"


def __str__(self):
    return f"Orthodox Drug"


class TraditionalDrug(models.Model):
    Product_Name = models.CharField(
        max_length=100, null=True, blank=True, db_column="Product Name"
    )
    Active_Ingredient = models.CharField(
        max_length=1000, null=True, blank=True, db_column="Active Ingredient"
    )
    Disease_Indications = models.CharField(
        max_length=1000, null=True, blank=True, db_column="Disease Indications"
    )
    Scientific_Literature_Reference = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        db_column="Scientific Literature Reference",
    )
    Adverse_Effects = models.CharField(
        max_length=1000, null=True, blank=True, db_column="Adverse Effects"
    )

    class Meta:
        db_table = "TraditionalDrug"
        app_label = "drugInfo"


def __str__(self):
    return f"Traditional Drug"
