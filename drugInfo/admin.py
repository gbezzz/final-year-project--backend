from django.contrib import admin
from .models import OrthodoxDrug, TraditionalDrug


class OrthodoxDrugAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "cas_number",
        "unii",
        "state",
        # "groups",
        # "general_references",
        # "synthesis_reference",
        # "indication",
        # "pharmacodynamics",
        # "mechanism_of_action",
        # "toxicity",
        # "metabolism",
        # "absorption",
        # "half_life",
        # "protein_binding",
        # "route_of_elimination",
        # "volume_of_distribution",
        # "clearance",
        # "classification",
        # "direct_parent",
        # "kingdom",
        # "superclass",
        # "class_field",
        # "subclass",
        # "salts",
        # "synonyms",
        # "products",
        # "international_brands",
        # "mixtures",
        # "packagers",
        # "manufacturers",
        # "prices",
        # "categories",
        # "affected_organisms",
        # "dosages",
        # "atc_codes",
        # "ahfs_codes",
        # "pdb_entries",
        # "patents",
        # "food_interactions",
        # "drug_interactions",
        # "sequences",
        # "experimental_properties",
        # "external_identifiers",
        # "external_links",
        # "pathways",
        # "reactions",
        # "snp_effects",
        # "snp_adverse_effects",
    )


admin.site.register(OrthodoxDrug, OrthodoxDrugAdmin)


class TraditionalDrugAdmin(admin.ModelAdmin):
    list_display = (
        "Product_Name",
        "Active_Ingredient",
        "Disease_Indications",
        "Scientific_Literature_Reference",
        "Adverse_Effects",
    )


admin.site.register(TraditionalDrug, TraditionalDrugAdmin)
