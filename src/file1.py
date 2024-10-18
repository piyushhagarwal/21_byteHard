from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_by = models.ForeignKey(
        User,
        verbose_name="created_by",
        related_name="admin_%(class)s_created_by",
        on_delete=models.PROTECT,
    )
    created_date_time = models.DateTimeField(
        verbose_name="Created Date Time", auto_now_add=True
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="updated_by",
        related_name="admin_%(class)s_updated_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    updated_date_time = models.DateTimeField(
        verbose_name="Updated Date Time", auto_now_add=False, blank=True, null=True
    )

    class Meta:
        abstract = True


class BasicModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        abstract = True


class CountryCurrency(BasicModel):
    country_name = models.CharField(max_length=50, verbose_name="Country Name")
    country_iso_code = models.CharField(max_length=10, verbose_name="Country ISO Code")
    country_code = models.CharField(
        blank=True, null=True, max_length=20, verbose_name="Country Code"
    )
    currency_code = models.CharField(
        blank=True, null=True, max_length=10, verbose_name="Currency Code"
    )
    currency_symbol = models.CharField(
        blank=True, null=True, max_length=10, verbose_name="Currency Sysmbol"
    )

    class Meta:
        db_table = "tbl_country_currency_mst"


class State(BasicModel):
    country_ref_id = models.ForeignKey(
        "CountryCurrency",
        on_delete=models.PROTECT,
        verbose_name="Country Ref Id",
        related_name="admin_states",
    )
    state_name = models.CharField(max_length=100, verbose_name="State Name")
    state_code = models.IntegerField(verbose_name="State Code")

    class Meta:
        db_table = "tbl_state_mst"


class District(BasicModel):
    state_ref_id = models.ForeignKey(
        "State",
        on_delete=models.PROTECT,
        verbose_name="State Ref Id",
        related_name="admin_district",
    )
    district_name = models.CharField(max_length=100, verbose_name="District Name")
    district_code = models.IntegerField(verbose_name="District Code")

    class Meta:
        db_table = "tbl_district_mst"


class Taluka(BasicModel):
    district_ref_id = models.ForeignKey(
        "District",
        on_delete=models.PROTECT,
        verbose_name="District Ref Id",
        related_name="admin_district_taluka",
    )
    sub_district_name = models.CharField(
        max_length=100, verbose_name="sub_district_name"
    )
    sub_district_code = models.IntegerField(verbose_name="Sub District Code")

    class Meta:
        db_table = "tbl_taluka_mst"


class Village(BasicModel):
    sub_district_ref_id = models.ForeignKey(
        Taluka,
        on_delete=models.PROTECT,
        verbose_name="sub_district_ref_id",
        related_name="admin_sub_district_village",
    )
    village_name = models.CharField(
        max_length=100, verbose_name="Village With Sub District Name"
    )
    village_code = models.IntegerField(verbose_name="Village Code")

    class Meta:
        db_table = "tbl_village_mst"


class AllMaster(BasicModel):
    master_type = models.CharField(max_length=50, verbose_name="Master Type")
    master_value = models.CharField(max_length=50, verbose_name="Master Value")
    master_key = models.CharField(max_length=50, verbose_name="Master Key")

    class Meta:
        db_table = "tbl_master"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class CalendarMst(BasicModel):
    calendar_type_id = models.ForeignKey(
        AllMaster, verbose_name="calendar_type_id", default=0, on_delete=models.CASCADE
    )  # Yearly, Monthly, Weekly, Daily, Quaterly

    class Meta:
        db_table = "tbl_calendar_mst"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


# calender will be generated for Previous 10 years, including current future 25 years
class CalendarDetails(BasicModel):
    mst_ref_id = models.ForeignKey(
        CalendarMst,
        verbose_name="mst_ref_id",
        related_name="admin_initialItemRow",
        on_delete=models.CASCADE,
        default=-1,
    )
    fiscal_year = models.CharField(verbose_name="fiscal_year", max_length=10)
    period = models.IntegerField(verbose_name="period")
    start_date = models.DateField(verbose_name="start_date", auto_now_add=False)
    end_date = models.DateField(verbose_name="end_date", auto_now_add=False)
    month = models.CharField(verbose_name="month", max_length=10)
    status = models.CharField(verbose_name="status", max_length=10)

    class Meta:
        db_table = "tbl_calendar_details"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


TENANT_STATUS_CHOICES = (
    ("Created", "Created"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
    ("Verified", "Verified"),
    ("SendBack", "SendBack"),
)


class Tenant(BaseModel):
    unique_id = models.CharField(max_length=20, verbose_name="unique_id")
    tenant_name = models.CharField(verbose_name="tenant_name", max_length=255)
    tenant_short_name = models.CharField(
        verbose_name="tenant_short_name", max_length=50, blank=True, null=True
    )
    ownership_status = models.ForeignKey(
        AllMaster,
        verbose_name="ownership_status",
        related_name="admin_ownership_status",
        on_delete=models.PROTECT,
    )

    contact_person_name = models.CharField(
        verbose_name="contact_person_name", max_length=255, blank=True, null=True
    )
    phone_no = models.CharField(verbose_name="phone_no", max_length=20)
    email_id = models.CharField(verbose_name="email_id", max_length=100)

    tenant_type_id = models.ForeignKey(
        AllMaster,
        verbose_name="tenant_type_id",
        related_name="admin_tenant_tenant_type_id",
        on_delete=models.PROTECT,
    )  # Entity Type ex: Agdi System, Federation, FPO/FPC...

    country = models.ForeignKey(
        CountryCurrency,
        verbose_name="country",
        related_name="admin_tenant_country",
        on_delete=models.PROTECT,
    )
    state = models.ForeignKey(
        State,
        verbose_name="state",
        related_name="admin_tenant_state",
        on_delete=models.PROTECT,
    )
    district = models.ForeignKey(
        District,
        verbose_name="district",
        related_name="admin_tenant_district",
        on_delete=models.PROTECT,
    )
    taluka = models.ForeignKey(
        Taluka,
        verbose_name="taluka",
        related_name="admin_tenant_taluka",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    address = models.CharField(verbose_name="address", max_length=500)
    address1 = models.CharField(
        verbose_name="address", max_length=500, blank=True, null=True
    )
    pin_code = models.CharField(verbose_name="pin_code", max_length=10)
    pan_no = models.CharField(verbose_name="pan_no", max_length=15)
    tan_no = models.CharField(
        verbose_name="tan_no", max_length=15, blank=True, null=True
    )
    gst_no = models.CharField(verbose_name="gst_no", max_length=15)
    cin_no = models.CharField(
        verbose_name="cin_no", max_length=21, blank=True, null=True
    )

    tenant_logo_path = models.CharField(
        verbose_name="tenant_logo_path", max_length=255, blank=True, null=True
    )
    header_image_details = models.TextField(
        verbose_name="header_image_details", blank=True, null=True
    )
    footer_image_details = models.TextField(
        verbose_name="footer_image_details", blank=True, null=True
    )
    header_text_details = models.TextField(
        verbose_name="header_text_details", blank=True, null=True
    )
    footer_text_details = models.TextField(
        verbose_name="footer_text_details", blank=True, null=True
    )
    header_image_position = models.CharField(
        max_length=50, verbose_name="header_image_position", blank=True, null=True
    )
    header_text_position = models.CharField(
        max_length=50, verbose_name="header_text_position", blank=True, null=True
    )
    footer_image_position = models.CharField(
        max_length=50, verbose_name="footer_image_position", blank=True, null=True
    )
    footer_text_position = models.CharField(
        max_length=50, verbose_name="footer_text_position", blank=True, null=True
    )
    header_image_type = models.CharField(
        max_length=50, verbose_name="header_image_type", blank=True, null=True
    )
    footer_image_type = models.CharField(
        max_length=50, verbose_name="footer_image_type", blank=True, null=True
    )

    import_code = models.CharField(
        verbose_name="import_code", max_length=20, blank=True, null=True
    )
    export_code = models.CharField(
        verbose_name="export_code", max_length=20, blank=True, null=True
    )

    # workflow_status = models.CharField(max_length=20, verbose_name="status", default="Created" ,choices=FARMER_STATUS_CHOICE)
    # remark = models.CharField(max_length=1000, verbose_name="remark", blank=True, null=True)
    # error_code_id = models.ForeignKey(ErrorCodeMst,verbose_name="error_code_id",blank=True,null=True, on_delete=models.PROTECT)
    # verified_by = models.ForeignKey(User,verbose_name="verified_by",related_name="admin_farmer_verified_by",blank=True,null=True, on_delete=models.PROTECT)
    # verified_role_id = models.ForeignKey(Roles, verbose_name="verified_role_id", on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table = "tbl_tenant_mst"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_name"],
                condition=models.Q(is_deleted=False),
                name="unique in tenant name not deleted",
            ),
            models.UniqueConstraint(
                fields=["phone_no"],
                condition=models.Q(is_deleted=False),
                name="unique in tenant phone_no not deleted",
            ),
        ]


REVISION_STATUS_CHOICES = (
    ("Effective", "Effective"),
    ("Future", "Future"),
    ("History", "History"),
)


# Membership/Subscription , applicable for FPC/FPO
class TenantContractDetails(BaseModel):
    mst_ref_id = models.ForeignKey(
        Tenant,
        default=0,
        verbose_name="mst_ref_id",
        related_name="admin_contract_details",
        on_delete=models.CASCADE,
    )

    from_date = models.DateField(verbose_name="from_date", auto_now_add=False)
    to_date = models.DateField(verbose_name="to_date", auto_now_add=False)
    revision_status = models.CharField(
        verbose_name="revision_status", max_length=20, choices=REVISION_STATUS_CHOICES
    )
    max_no_of_users = models.IntegerField(verbose_name="max_no_of_user")
    concurent_user = models.CharField(verbose_name="concurent_user", max_length=15)
    api_limit = models.CharField(verbose_name="api_limit", max_length=15)
    api_calls_blocked_for_in_minutes = models.CharField(
        verbose_name="api_calls_blocked_for_in_minutes", max_length=15
    )
    application_blocking_in_minutes = models.CharField(
        verbose_name="application_blocking_in_minutes", max_length=15
    )

    class Meta:
        db_table = "tbl_tenant_contract_details"


class TenantContactDetails(BaseModel):
    mst_ref_id = models.ForeignKey(
        Tenant,
        default=0,
        verbose_name="mst_ref_id",
        on_delete=models.CASCADE,
        related_name="admin_contact_details",
    )

    full_name = models.CharField(max_length=255, verbose_name="full_name")
    phone_no = models.CharField(max_length=20, verbose_name="phone_no")
    email = models.CharField(max_length=355, verbose_name="email")

    department = models.CharField(
        verbose_name="department", max_length=50, blank=True, null=True
    )  # department
    sub_department = models.CharField(
        verbose_name="sub_department", max_length=50, blank=True, null=True
    )  # sub_department
    designation = models.CharField(
        max_length=50, verbose_name="designation", blank=True, null=True
    )

    class Meta:
        db_table = "tbl_tenant_contact_details"


class TenantKycAttachment(BaseModel):
    mst_ref_id = models.ForeignKey(
        Tenant,
        verbose_name="mst_ref_id",
        related_name="admin_kyc_details",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    document_name = models.ForeignKey(
        AllMaster,
        verbose_name="document_name",
        related_name="admin_document_name",
        on_delete=models.PROTECT,
    )  # Pan, GSTIN, Udyam aadhar
    document_seq_number = models.CharField(
        verbose_name="document_number", max_length=20
    )
    document_path = models.CharField(verbose_name="document_path", max_length=255)

    class Meta:
        db_table = "tbl_tenant_kyc_attachment"


class TenantStructure(BaseModel):
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="tenant",
        related_name="admin_tenant_structure_tenant_id",
        on_delete=models.PROTECT,
    )
    parent_tenant = models.ForeignKey(
        Tenant,
        verbose_name="parent_tenant",
        related_name="admin_tenant_structure_parent_tenant_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    tenant_level = models.IntegerField(verbose_name="tenant_level")

    class Meta:
        db_table = "tbl_tenant_structure"


class TenantHierarchyMapping(BaseModel):
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="tenant",
        related_name="admin_tenant_hierarchy_tenant_id",
        on_delete=models.PROTECT,
    )
    tenant_structure = models.ForeignKey(
        TenantStructure,
        verbose_name="tenant_structure",
        related_name="admin_tenant_structure",
        on_delete=models.PROTECT,
    )
    parent_tenant = models.ForeignKey(
        Tenant,
        verbose_name="parent_tenant",
        related_name="admin_tenant_hierarchy_parent_tenant_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    parent_tenant_structure = models.ForeignKey(
        TenantStructure,
        verbose_name="parent_tenant_structure",
        related_name="admin_parent_tenant_structure",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "tbl_tenant_hierarchy_mapping"


class ScreenHierarchy(BasicModel):
    attribute_name = models.CharField(verbose_name="attribute_name", max_length=50)
    attribute_level = models.IntegerField(verbose_name="attribute_level")
    parent_attribute_name = models.CharField(
        verbose_name="parent_attribute_name", max_length=50
    )
    parent_attribute_level = models.IntegerField(verbose_name="parent_attribute_level")

    master_table_name = models.CharField(
        verbose_name="master_table_name", max_length=100
    )
    detail_table_name = models.CharField(
        verbose_name="detail_table_name", max_length=100, blank=True, null=True
    )
    sub_detail_table_name = models.CharField(
        verbose_name="sub_detail_table_name", max_length=100, blank=True, null=True
    )
    prev_attribute_name = models.CharField(
        verbose_name="prev_attribute_name", max_length=50, blank=True, null=True
    )
    next_attribute_name = models.CharField(
        verbose_name="next_attribute_name", max_length=50, blank=True, null=True
    )

    is_applicable_in_allocation = models.BooleanField(
        verbose_name="is_applicable_in_allocation", default=False
    )
    is_applicable_in_system_allocation = models.BooleanField(
        verbose_name="is_applicable_in_allocation", default=False
    )
    stepper_module_name = models.CharField(
        verbose_name="stepper_module_name", max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "tbl_screen_hierarchy"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class ScreenHierarchyDetail(BasicModel):
    screen_hierarchy_ref_id = models.ForeignKey(
        ScreenHierarchy,
        verbose_name="screen_hierarchy_ref_id",
        default=0,
        on_delete=models.PROTECT,
        related_name="admin_screenhierarchydetails_set",
    )
    attribute_name = models.CharField(verbose_name="attribute_name", max_length=50)
    detail_table_name = models.CharField(
        verbose_name="detail_table_name", max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "tbl_screen_hierarchy_detail"


class ScreenDefinition(BasicModel):
    screen_hierarchy_ref_id = models.ForeignKey(
        ScreenHierarchy,
        verbose_name="screen_hierarchy_ref_id",
        default=0,
        on_delete=models.PROTECT,
    )
    field_label = models.CharField(verbose_name="field_label", max_length=100)
    field_type = models.ForeignKey(
        AllMaster, verbose_name="field_type", on_delete=models.PROTECT
    )
    field_key = models.CharField(verbose_name="field_key", max_length=50)
    is_visible_in_mat_table = models.BooleanField(
        verbose_name="is_visible_in_mat_table", default=False
    )

    field_max_length = models.IntegerField(verbose_name="field_max_length", default=0)
    field_placeholder = models.CharField(
        verbose_name="field_placeholder", max_length=50, blank=True, null=True
    )
    sortby = models.IntegerField(verbose_name="sortby")
    is_onchange_event = models.BooleanField(
        verbose_name="is_onchange_event", default=False, blank=True, null=True
    )
    is_required = models.BooleanField(verbose_name="is_required", default=False)
    is_disabled = models.BooleanField(verbose_name="is_disabled", default=False)
    is_readonly = models.BooleanField(verbose_name="is_readonly", default=False)
    file_max_size = models.IntegerField(
        verbose_name="file_max_size", default=0, blank=True, null=True
    )  # in kb
    file_format = models.CharField(
        verbose_name="file_format", max_length=100, blank=True, null=True
    )

    dropdown_raw_query = models.TextField(
        verbose_name="dropdown_raw_query", blank=True, null=True
    )
    dropdown_table_name = models.CharField(
        verbose_name="file_format", max_length=100, blank=True, null=True
    )
    dropdown_option_tag_value = models.CharField(
        verbose_name="dropdown_option_tag_value", max_length=30, blank=True, null=True
    )
    dropdown_option_tag_label = models.CharField(
        verbose_name="dropdown_option_tag_label", max_length=30, blank=True, null=True
    )
    dropdown_groupby_column_name = models.CharField(
        verbose_name="dropdown_groupby_column_name",
        max_length=100,
        blank=True,
        null=True,
    )
    dropdown_orderby_column_name = models.CharField(
        verbose_name="dropdown_orderby_column_name",
        max_length=100,
        blank=True,
        null=True,
    )
    is_unique = models.BooleanField(verbose_name="is_unique", default=False)
    is_expandable = models.BooleanField(verbose_name="is_expandable", default=False)
    toggle_on_field_label = models.CharField(
        max_length=10, verbose_name="toggle_on_field_label", blank=True, null=True
    )
    toggle_off_field_label = models.CharField(
        max_length=10, verbose_name="toggle_off_field_label", blank=True, null=True
    )
    is_onchange_concatenate = models.BooleanField(
        default=False, verbose_name="is_onchange_concatenate"
    )
    onchange_concatenate_field_name = models.CharField(
        max_length=255,
        verbose_name="onchange_concatenate_field_name",
        blank=True,
        null=True,
    )
    onchange_concatenate_value = models.CharField(
        max_length=255, verbose_name="onchange_concatenate_value", blank=True, null=True
    )
    validator_name1 = models.CharField(
        max_length=100,
        verbose_name="validator_name1",
        blank=True,
        null=True,
    )
    validator_value1 = models.CharField(
        max_length=100,
        verbose_name="validator_value1",
        blank=True,
        null=True,
    )
    validator_html_value1 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value1",
        blank=True,
        null=True,
    )
    validator_name2 = models.CharField(
        max_length=100,
        verbose_name="validator_name2",
        blank=True,
        null=True,
    )
    validator_value2 = models.CharField(
        max_length=100,
        verbose_name="validator_value2",
        blank=True,
        null=True,
    )
    validator_html_value2 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value2",
        blank=True,
        null=True,
    )
    validator_name3 = models.CharField(
        max_length=100,
        verbose_name="validator_name3",
        blank=True,
        null=True,
    )
    validator_value3 = models.CharField(
        max_length=100,
        verbose_name="validator_value3",
        blank=True,
        null=True,
    )
    validator_html_value3 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value3",
        blank=True,
        null=True,
    )
    validator_name4 = models.CharField(
        max_length=100,
        verbose_name="validator_name4",
        blank=True,
        null=True,
    )
    validator_value4 = models.CharField(
        max_length=100,
        verbose_name="validator_value4",
        blank=True,
        null=True,
    )
    validator_html_value4 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value4",
        blank=True,
        null=True,
    )
    validator_name5 = models.CharField(
        max_length=100,
        verbose_name="validator_name5",
        blank=True,
        null=True,
    )
    validator_value5 = models.CharField(
        max_length=100,
        verbose_name="validator_value5",
        blank=True,
        null=True,
    )
    validator_html_value5 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value5",
        blank=True,
        null=True,
    )
    validator_name6 = models.CharField(
        max_length=100,
        verbose_name="validator_name6",
        blank=True,
        null=True,
    )
    validator_value6 = models.CharField(
        max_length=100,
        verbose_name="validator_value6",
        blank=True,
        null=True,
    )
    validator_html_value6 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value6",
        blank=True,
        null=True,
    )
    validator_name7 = models.CharField(
        max_length=100,
        verbose_name="validator_name7",
        blank=True,
        null=True,
    )
    validator_value7 = models.CharField(
        max_length=100,
        verbose_name="validator_value7",
        blank=True,
        null=True,
    )
    validator_html_value7 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value7",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "tbl_screen_defination"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class ScreenDefinitionDetails(BasicModel):
    screen_hierarchy_ref_id = models.ForeignKey(
        ScreenHierarchy,
        verbose_name="screen_hierarchy_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    screen_hierarchy_detail_ref_id = models.ForeignKey(
        ScreenHierarchyDetail,
        verbose_name="screen_hierarchy_detail_ref_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    field_label = models.CharField(verbose_name="field_label", max_length=100)
    field_type = models.ForeignKey(
        AllMaster, verbose_name="field_type", on_delete=models.PROTECT
    )
    field_key = models.CharField(verbose_name="field_key", max_length=50)

    field_max_length = models.IntegerField(verbose_name="field_max_length", default=0)
    field_placeholder = models.CharField(
        verbose_name="field_placeholder", max_length=50, blank=True, null=True
    )
    sortby = models.IntegerField(verbose_name="sortby")
    is_onchange_event = models.BooleanField(
        verbose_name="is_onchange_event", default=False
    )
    is_required = models.BooleanField(verbose_name="is_required", default=False)
    is_disabled = models.BooleanField(verbose_name="is_disabled", default=False)
    is_readonly = models.BooleanField(verbose_name="is_readonly", default=False)
    file_max_size = models.IntegerField(
        verbose_name="file_max_size", default=0, blank=True, null=True
    )  # in kb
    file_format = models.CharField(
        verbose_name="file_format", max_length=100, blank=True, null=True
    )

    dropdown_raw_query = models.TextField(
        verbose_name="dropdown_raw_query", blank=True, null=True
    )
    dropdown_table_name = models.CharField(
        verbose_name="file_format", max_length=100, blank=True, null=True
    )
    dropdown_option_tag_value = models.CharField(
        verbose_name="dropdown_option_tag_value", max_length=30, blank=True, null=True
    )
    dropdown_option_tag_label = models.CharField(
        verbose_name="dropdown_option_tag_label", max_length=30, blank=True, null=True
    )
    dropdown_groupby_column_name = models.CharField(
        verbose_name="dropdown_groupby_column_name",
        max_length=100,
        blank=True,
        null=True,
    )
    dropdown_orderby_column_name = models.CharField(
        verbose_name="dropdown_orderby_column_name",
        max_length=100,
        blank=True,
        null=True,
    )
    is_expandable = models.BooleanField(verbose_name="is_expandable", default=False)
    toggle_on_field_label = models.CharField(
        max_length=10, verbose_name="toggle_on_field_label", blank=True, null=True
    )
    toggle_off_field_label = models.CharField(
        max_length=10, verbose_name="toggle_off_field_label", blank=True, null=True
    )
    is_onchange_concatenate = models.BooleanField(
        default=False, verbose_name="is_onchange_concatenate"
    )
    onchange_concatenate_field_name = models.CharField(
        max_length=255,
        verbose_name="onchange_concatenate_field_name",
        blank=True,
        null=True,
    )
    onchange_concatenate_value = models.CharField(
        max_length=255, verbose_name="onchange_concatenate_value", blank=True, null=True
    )
    validator_name1 = models.CharField(
        max_length=100,
        verbose_name="validator_name1",
        blank=True,
        null=True,
    )
    validator_value1 = models.CharField(
        max_length=100,
        verbose_name="validator_value1",
        blank=True,
        null=True,
    )
    validator_html_value1 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value1",
        blank=True,
        null=True,
    )
    validator_name2 = models.CharField(
        max_length=100,
        verbose_name="validator_name2",
        blank=True,
        null=True,
    )
    validator_value2 = models.CharField(
        max_length=100,
        verbose_name="validator_value2",
        blank=True,
        null=True,
    )
    validator_html_value2 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value2",
        blank=True,
        null=True,
    )
    validator_name3 = models.CharField(
        max_length=100,
        verbose_name="validator_name3",
        blank=True,
        null=True,
    )
    validator_value3 = models.CharField(
        max_length=100,
        verbose_name="validator_value3",
        blank=True,
        null=True,
    )
    validator_html_value3 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value3",
        blank=True,
        null=True,
    )
    validator_name4 = models.CharField(
        max_length=100,
        verbose_name="validator_name4",
        blank=True,
        null=True,
    )
    validator_value4 = models.CharField(
        max_length=100,
        verbose_name="validator_value4",
        blank=True,
        null=True,
    )
    validator_html_value4 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value4",
        blank=True,
        null=True,
    )
    validator_name5 = models.CharField(
        max_length=100,
        verbose_name="validator_name5",
        blank=True,
        null=True,
    )
    validator_value5 = models.CharField(
        max_length=100,
        verbose_name="validator_value5",
        blank=True,
        null=True,
    )
    validator_html_value5 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value5",
        blank=True,
        null=True,
    )
    validator_name6 = models.CharField(
        max_length=100,
        verbose_name="validator_name6",
        blank=True,
        null=True,
    )
    validator_value6 = models.CharField(
        max_length=100,
        verbose_name="validator_value6",
        blank=True,
        null=True,
    )
    validator_html_value6 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value6",
        blank=True,
        null=True,
    )
    validator_name7 = models.CharField(
        max_length=100,
        verbose_name="validator_name7",
        blank=True,
        null=True,
    )
    validator_value7 = models.CharField(
        max_length=100,
        verbose_name="validator_value7",
        blank=True,
        null=True,
    )
    validator_html_value7 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value7",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "tbl_screen_defination_details"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class ScreenDefinitionSubDetails(BasicModel):
    screen_hierarchy_ref_id = models.ForeignKey(
        ScreenHierarchy,
        verbose_name="screen_hierarchy_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    field_label = models.CharField(verbose_name="field_label", max_length=100)
    field_type = models.ForeignKey(
        AllMaster, verbose_name="field_type", on_delete=models.PROTECT
    )
    field_key = models.CharField(verbose_name="field_key", max_length=50)

    field_max_length = models.IntegerField(verbose_name="field_max_length", default=0)
    field_placeholder = models.CharField(
        verbose_name="field_placeholder", max_length=50, blank=True, null=True
    )
    sortby = models.IntegerField(verbose_name="sortby")
    is_onchange_event = models.BooleanField(
        verbose_name="is_onchange_event", default=False
    )
    is_required = models.BooleanField(verbose_name="is_required", default=False)
    is_disabled = models.BooleanField(verbose_name="is_disabled", default=False)
    is_readonly = models.BooleanField(verbose_name="is_readonly", default=False)
    file_max_size = models.IntegerField(
        verbose_name="file_max_size", default=0, blank=True, null=True
    )  # in kb
    file_format = models.CharField(
        verbose_name="file_format", max_length=100, blank=True, null=True
    )

    dropdown_raw_query = models.TextField(
        verbose_name="dropdown_raw_query", blank=True, null=True
    )
    dropdown_table_name = models.CharField(
        verbose_name="file_format", max_length=100, blank=True, null=True
    )
    dropdown_option_tag_value = models.CharField(
        verbose_name="dropdown_option_tag_value", max_length=30, blank=True, null=True
    )
    dropdown_option_tag_label = models.CharField(
        verbose_name="dropdown_option_tag_label", max_length=30, blank=True, null=True
    )
    dropdown_groupby_column_name = models.CharField(
        verbose_name="dropdown_groupby_column_name",
        max_length=100,
        blank=True,
        null=True,
    )
    dropdown_orderby_column_name = models.CharField(
        verbose_name="dropdown_orderby_column_name",
        max_length=100,
        blank=True,
        null=True,
    )
    toggle_on_field_label = models.CharField(
        max_length=10, verbose_name="toggle_on_field_label", blank=True, null=True
    )
    toggle_off_field_label = models.CharField(
        max_length=10, verbose_name="toggle_off_field_label", blank=True, null=True
    )
    is_onchange_concatenate = models.BooleanField(
        default=False, verbose_name="is_onchange_concatenate"
    )
    onchange_concatenate_field_name = models.CharField(
        max_length=255,
        verbose_name="onchange_concatenate_field_name",
        blank=True,
        null=True,
    )
    onchange_concatenate_value = models.CharField(
        max_length=255, verbose_name="onchange_concatenate_value", blank=True, null=True
    )

    validator_name1 = models.CharField(
        max_length=100,
        verbose_name="validator_name1",
        blank=True,
        null=True,
    )
    validator_value1 = models.CharField(
        max_length=100,
        verbose_name="validator_value1",
        blank=True,
        null=True,
    )
    validator_html_value1 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value1",
        blank=True,
        null=True,
    )
    validator_name2 = models.CharField(
        max_length=100,
        verbose_name="validator_name2",
        blank=True,
        null=True,
    )
    validator_value2 = models.CharField(
        max_length=100,
        verbose_name="validator_value2",
        blank=True,
        null=True,
    )
    validator_html_value2 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value2",
        blank=True,
        null=True,
    )
    validator_name3 = models.CharField(
        max_length=100,
        verbose_name="validator_name3",
        blank=True,
        null=True,
    )
    validator_value3 = models.CharField(
        max_length=100,
        verbose_name="validator_value3",
        blank=True,
        null=True,
    )
    validator_html_value3 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value3",
        blank=True,
        null=True,
    )
    validator_name4 = models.CharField(
        max_length=100,
        verbose_name="validator_name4",
        blank=True,
        null=True,
    )
    validator_value4 = models.CharField(
        max_length=100,
        verbose_name="validator_value4",
        blank=True,
        null=True,
    )
    validator_html_value4 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value4",
        blank=True,
        null=True,
    )
    validator_name5 = models.CharField(
        max_length=100,
        verbose_name="validator_name5",
        blank=True,
        null=True,
    )
    validator_value5 = models.CharField(
        max_length=100,
        verbose_name="validator_value5",
        blank=True,
        null=True,
    )
    validator_html_value5 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value5",
        blank=True,
        null=True,
    )
    validator_name6 = models.CharField(
        max_length=100,
        verbose_name="validator_name6",
        blank=True,
        null=True,
    )
    validator_value6 = models.CharField(
        max_length=100,
        verbose_name="validator_value6",
        blank=True,
        null=True,
    )
    validator_html_value6 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value6",
        blank=True,
        null=True,
    )
    validator_name7 = models.CharField(
        max_length=100,
        verbose_name="validator_name7",
        blank=True,
        null=True,
    )
    validator_value7 = models.CharField(
        max_length=100,
        verbose_name="validator_value7",
        blank=True,
        null=True,
    )
    validator_html_value7 = models.CharField(
        max_length=100,
        verbose_name="validator_html_value7",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "tbl_screen_defination_sub_details"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class ScreenDefinitionMapping(BasicModel):
    screen_hierarchy_ref_id = models.ForeignKey(
        ScreenHierarchy,
        verbose_name="screen_hierarchy_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    screen_field_ref_id = models.ForeignKey(
        ScreenDefinition,
        verbose_name="screen_field_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    parameter_name = models.CharField(verbose_name="parameter_name", max_length=100)

    class Meta:
        db_table = "tbl_screen_defination_mapping"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class ScreenDefinitionDetailsMapping(BasicModel):
    screen_hierarchy_ref_id = models.ForeignKey(
        ScreenHierarchy,
        verbose_name="screen_hierarchy_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    screen_field_ref_id = models.ForeignKey(
        ScreenDefinitionDetails,
        verbose_name="screen_field_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    parameter_name = models.CharField(verbose_name="parameter_name", max_length=100)

    class Meta:
        db_table = "tbl_screen_definition_details_mapping"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class ScreenDefinitionSubDetailsMapping(BasicModel):
    screen_hierarchy_ref_id = models.ForeignKey(
        ScreenHierarchy,
        verbose_name="screen_hierarchy_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    screen_field_ref_id = models.ForeignKey(
        ScreenDefinitionSubDetails,
        verbose_name="screen_field_ref_id",
        default=-1,
        on_delete=models.PROTECT,
    )
    parameter_name = models.CharField(verbose_name="parameter_name", max_length=100)

    class Meta:
        db_table = "tbl_screen_definition_sub_details_mapping"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class Employee(BaseModel):
    tenant_id = models.ForeignKey(
        Tenant, verbose_name="tenant_id", on_delete=models.CASCADE
    )
    unique_id = models.CharField(max_length=20, verbose_name="unique_id")

    emp_name = models.CharField(max_length=255, verbose_name="First name")
    email = models.EmailField(max_length=355, verbose_name="Email")
    phone = models.CharField(
        max_length=20, verbose_name="Phone Number", blank=True, null=True
    )

    designation = models.IntegerField(
        verbose_name="designation"
    )  # fetch from dynamic table designation
    department = models.IntegerField(
        verbose_name="department"
    )  # fetch from dynamic table department
    sub_department = models.IntegerField(
        verbose_name="sub_department"
    )  # fetch from dynamic table sub_department

    maker_checker = models.ForeignKey(
        AllMaster, verbose_name="authority", on_delete=models.PROTECT
    )

    class Meta:
        db_table = "tbl_employee_mst"


class Login(BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name="user",
        related_name="admin_login_user_id",
        on_delete=models.PROTECT,
    )
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="tenant",
        related_name="admin_login_tenant_id",
        on_delete=models.PROTECT,
    )
    employee = models.ForeignKey(
        Employee,
        verbose_name="employee",
        related_name="admin_login_employee_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    is_password_change = models.BooleanField(
        verbose_name="is_password_change", default=False
    )

    is_user_blocked = models.BooleanField(default=False, verbose_name="is_user_blocked")
    user_blocked_time = models.DateTimeField(
        blank=True, null=True, verbose_name="User Blocked Time"
    )
    security_code = models.IntegerField(
        verbose_name="User Account Security Code", default=0
    )
    cool_down_timestamp = models.DateTimeField(
        blank=True, null=True, verbose_name="Retry Cool Down DateTimeStamp"
    )
    is_loggedin = models.BooleanField(default=False, verbose_name="is_loggedin")
    auth_token = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="auth_token"
    )
    retry_count = models.IntegerField(default=0, verbose_name="Retry Count")

    class Meta:
        db_table = "tbl_login_mst"


class Role(BaseModel):
    role_name = models.CharField(verbose_name="role_name", max_length=150)
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="tenant",
        related_name="admin_role_tenant_id",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = "tbl_role_mst"


class UserRole(BaseModel):
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="tenant",
        related_name="admin_user_role_tenant_id",
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        User,
        verbose_name="user",
        related_name="admin_user_role_user_id",
        on_delete=models.PROTECT,
    )
    role = models.ForeignKey(
        Role,
        verbose_name="role",
        related_name="admin_user_role_role_id",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = "tbl_user_role"


class UserRoleDetails(BaseModel):
    header_ref_id = models.ForeignKey(
        UserRole,
        default=0,
        verbose_name="Header Ref ID",
        on_delete=models.CASCADE,
        related_name="admin_initialItemRow",
    )
    attribute_ref_id = models.ForeignKey(
        "ScreenHierarchy",
        verbose_name="attribute_ref_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    attribute_field_ref_id = models.ForeignKey(
        "ScreenDefinition",
        verbose_name="attribute_field_ref_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    field_name = models.CharField(max_length=50, verbose_name="field_name")
    field_value = models.CharField(max_length=50, verbose_name="field_value")

    class Meta:
        db_table = "tbl_user_roles_details"


class UserDetails(models.Model):
    user_id = models.ForeignKey(
        User,
        verbose_name="User Id",
        on_delete=models.PROTECT,
        related_name="admin_user_data",
    )
    profile_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="profile_name"
    )
    retry_count = models.IntegerField(default=0, verbose_name="Retry Count")
    is_user_blocked = models.BooleanField(default=False, verbose_name="is_user_blocked")
    user_blocked_time = models.DateTimeField(
        blank=True, null=True, verbose_name="User Blocked Time"
    )
    security_code = models.IntegerField(verbose_name="User Account Security Code")
    email = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="User Email"
    )
    cool_down_timestamp = models.DateTimeField(
        blank=True, null=True, verbose_name="Retry Cool Down DateTimeStamp"
    )
    is_loggedin = models.BooleanField(default=False, verbose_name="is_loggedin")
    auth_token = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="auth_token"
    )
    created_date_time = models.DateTimeField(
        verbose_name="UserDetails created_date_time", auto_now_add=True
    )

    class Meta:
        db_table = "tbl_user_details"


class ApiRole(BaseModel):
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="tenant",
        related_name="admin_api_role_tenant_id",
        on_delete=models.PROTECT,
    )
    role = models.ForeignKey(
        Role,
        verbose_name="role",
        related_name="admin_api_role_role_id",
        on_delete=models.PROTECT,
    )
    api_url = models.CharField(verbose_name="api_url", max_length=50)
    allowed_methods = models.CharField(verbose_name="allowed_methods", max_length=20)

    class Meta:
        db_table = "tbl_api_role"


class LeftPanel(BaseModel):
    form_name = models.CharField(verbose_name="form_name", max_length=100)
    form_link = models.CharField(
        verbose_name="form_link", max_length=200, blank=True, null=True
    )
    module_path = models.CharField(verbose_name="module_path", max_length=500)

    is_parent = models.CharField(verbose_name="is_parent", max_length=1, default="N")
    is_child = models.CharField(verbose_name="is_child", max_length=1, default="N")
    is_sub_child = models.CharField(
        verbose_name="is_sub_child", max_length=1, default="N"
    )

    parent_code = models.CharField(verbose_name="parent_code", max_length=50)
    child_code = models.CharField(
        verbose_name="child_code", max_length=50, blank=True, null=True
    )
    sub_child_code = models.CharField(
        verbose_name="sub_child_code", max_length=100, blank=True, null=True
    )
    icon_class = models.CharField(
        verbose_name="icon_class", max_length=20, blank=True, null=True
    )
    sequence_id = models.IntegerField(verbose_name="sequence_id", default=0)
    group_title = models.CharField(
        verbose_name="group_title", max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "tbl_left_panel"

        
class PagesRole(BaseModel):
    form = models.ForeignKey(
        LeftPanel,
        verbose_name="form",
        related_name="pages_role_faorm_id",
        on_delete=models.PROTECT,
    )
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="tenant",
        related_name="pages_role_tenant_id",
        on_delete=models.PROTECT,
    )
    role = models.ForeignKey(
        Role,
        verbose_name="role",
        related_name="pages_role_role_id",
        on_delete=models.PROTECT,
    )

    read_access = models.CharField(
        verbose_name="read_access", max_length=1, default="N"
    )
    write_access = models.CharField(
        verbose_name="write_access", max_length=1, default="N"
    )
    delete_access = models.CharField(
        verbose_name="delete_access", max_length=1, default="N"
    )

    class Meta:
        db_table = "tbl_pages_role"



class PagesApi(BaseModel):
    form = models.ForeignKey(
        LeftPanel,
        verbose_name="form",
        related_name="admin_pages_api_faorm_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    api_url = models.CharField(verbose_name="api_url", max_length=50)

    class Meta:
        db_table = "tbl_pages_api"


class Events(BaseModel):
    tenant_id = models.ForeignKey(
        Tenant,
        verbose_name="tenant_id",
        on_delete=models.PROTECT,
    )
    event_name = models.CharField(max_length=100, verbose_name="event_name")
    event_description = models.TextField(
        verbose_name="event_description", blank=True, null=True
    )
    location = models.CharField(verbose_name="location_ref_id",null=True, max_length=255) # Dynamic Location FK

    event_date = models.DateField(verbose_name="event_date")
    event_start_time = models.TimeField(verbose_name="event_start_time")
    event_end_time = models.TimeField(verbose_name="event_end_time")
    event_poster_image_path = models.CharField(
        max_length=255, verbose_name="event_poster_image_path"
    )
    fpc_ref_id = models.ForeignKey(
        Tenant,
        verbose_name="tenant_id",
        on_delete=models.PROTECT,
        related_name="admin_fpc_ref_id",
        blank=True,
        null=True,
    )
    district_ref_id = models.ForeignKey(
        District,
        verbose_name="district_ref_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    taluka_ref_id = models.ForeignKey(
        Taluka,
        verbose_name="taluka_ref_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    pin_code = models.CharField(
        verbose_name="pin_code", max_length=10, blank=True, null=True
    )
    organiser_details = models.TextField(
        verbose_name="organiser_details", blank=True, null=True
    )
    is_approved = models.BooleanField(
        verbose_name="is_approved", default=None, blank=True, null=True
    )
    event_type = models.CharField(verbose_name="pin_code", max_length=25, default='Event')

    class Meta:
        db_table = "tbl_events"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class EventsDataCollection(BaseModel):
    tenant_id = models.ForeignKey(
        Tenant,
        verbose_name="tenant_id",
        on_delete=models.PROTECT,
    )
    event_ref_id = models.ForeignKey(
        Events,
        verbose_name="tenant_id",
        on_delete=models.PROTECT,
    )
    farmer_name = models.CharField(max_length=255, verbose_name="Farmer name", blank=True, null=True)
    farmer_email = models.EmailField(max_length=355, verbose_name="Farmer Email", blank=True, null=True)
    farmer_phone = models.CharField(
        max_length=20, verbose_name="Farmer Phone Number", blank=True, null=True
    ) 

    class Meta:
        db_table = "tbl_events_data_collection"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()


class MultiTenantUserMappingMaster(BaseModel):
    username = models.CharField(max_length=50, verbose_name="Username")
    password = models.CharField(max_length=50, verbose_name="Passowrd")


    tenant_ref_id = models.ForeignKey(
        Tenant,
        verbose_name="tenant_ref_id",
        related_name="admin_%(class)s_tenant_ref_id",
        on_delete=models.PROTECT,
        default="1",
    )
    is_system_generated_admin = models.BooleanField(
        verbose_name="SFTP Location", default=False, blank=True, null=True
    )

    class Meta:
        db_table = "tbl_multi_tenant_user_mapping_master"


class MultiTenantAllDatabasesMappingMaster(BaseModel):
    tenant_key = models.CharField(max_length=350, verbose_name="tenant_key")
    tenant_name = models.CharField(max_length=350, verbose_name="tenant_name")
    tenant_db_name = models.CharField(
        max_length=350, verbose_name="tenant database_user name"
    )
    parent_id = models.IntegerField(
        default=None, null=True, blank=True, verbose_name="Parent_id refrence"
    )
    profile_logo_image = models.CharField(
        verbose_name="profile_logo_image", max_length=255, blank=True, null=True
    )
    is_parent = models.BooleanField(
        verbose_name="SFTP Location", default=False, blank=True, null=True
    )
    tenant_ref_id = models.ForeignKey(
        Tenant,
        verbose_name="tenant_ref_id",
        related_name="admin_%(class)s_tenant_ref_id",
        on_delete=models.PROTECT,
        default="1",
    )

    class Meta:
        db_table = "tbl_multi_tenant_all_databases_mapping_master"






class SubscriptionPlanMst(BaseModel):
    plan_name = models.CharField(verbose_name="plan_name", max_length=255)
    plan_description = models.CharField(
        verbose_name="plan_description", max_length=255, blank=True, null=True
    )
    plan_code = models.CharField(verbose_name="plan_code", max_length=255)
    plan_charges = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="plan_charges",
        default=0,
    )
    max_device = models.IntegerField(default=0,verbose_name="Max Device") #if 0 then unlimited devices
    device_type_ref_id = models.ForeignKey(
        AllMaster, verbose_name="device_type_ref_id",related_name="device_type_ref_id", on_delete=models.CASCADE
    ) #web, mobile, all devices
    country_ref_id = models.ForeignKey(
        "CountryCurrency",
        verbose_name="country",
        related_name="country_ref_id",
        on_delete=models.PROTECT,
    )
    frequency_in_days = models.ForeignKey(
        AllMaster,
        verbose_name="frequency_in_days",related_name="frequency_in_days",  on_delete=models.CASCADE 
    ) #30 days,90days,180 days,365 days
    is_recurring = models.BooleanField(
        verbose_name="Is Recurring", default=True
    )

    plan_type_ref_id = models.ForeignKey(
        AllMaster, verbose_name="plan_type_ref_id", related_name="plan_type_ref_id", default=0, on_delete=models.CASCADE
    )  # FPC, Federation,Farmer,Adhoc
    from_date = models.DateField(verbose_name="From Date",auto_now_add=False)
    to_date = models.DateField(verbose_name="To Date",auto_now_add=False)
    revision_status = models.CharField(max_length=20,verbose_name="Revision Status")
    is_recommended_plan = models.BooleanField(
        verbose_name="Is Recommended Plan", default=False, null=True
    )
    is_display_plan = models.BooleanField(
        verbose_name="Is Display Plan", default=False, null=True
    )

    class Meta:
        db_table = "tbl_subscription_plan_mst"




class SubscriptionPlanDetails(BaseModel):
    mst_ref_id = models.ForeignKey(
        SubscriptionPlanMst,
        verbose_name="submst_ref_id",
        related_name="subscription_feature_plan_details",
        on_delete=models.CASCADE,
        default=0
    )
    feature_name = models.IntegerField(verbose_name="feature_name") #FK from dynamic_models_subscription_features -> name, description ,key
    feature_type_ref_id = models.ForeignKey(
        AllMaster, verbose_name="feature_type_ref_id", on_delete=models.CASCADE
    ) #text, corrected,dashed, wrong
    feature_description = models.CharField(
        verbose_name="feature_description", max_length=255
    )
    class Meta:
        db_table = "tbl_subscription_plan_details"


class SubscriptionPlanLeftPanelDetails(BaseModel):
    mst_ref_id = models.ForeignKey(
        SubscriptionPlanMst,
        verbose_name="subscriptionmst_ref_id",
        related_name="subscription_plan_details",
        on_delete=models.CASCADE,
        default=0
    )
    form_ref_id = models.ForeignKey(
        LeftPanel, verbose_name="form_ref_id", on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = "tbl_subscription_plan_left_panel_details"





class TenantOnboardTemp(BaseModel):
    tenant_name = models.CharField(verbose_name="tenant_onboard_name", max_length=255)
    tenant_short_name = models.CharField(
        verbose_name="tenant_onboard_short_name", max_length=50, blank=True, null=True
    )

    contact_person_name = models.CharField(
        verbose_name="tenant_onboardcontact_person_name",
        max_length=255,
        blank=True,
        null=True,
    )
    phone_no = models.CharField(verbose_name="phone_no", max_length=20)
    email_id = models.CharField(verbose_name="email_id", max_length=100)

    tenant_type_id = models.ForeignKey(
        AllMaster,
        verbose_name="tenant_onboardtenant_type_id",
        related_name="tenant_onboard_type_id",
        on_delete=models.PROTECT,
    )  # Entity Type ex: Agdi System, Federation, FPO/FPC...

    country = models.ForeignKey(
        CountryCurrency,
        verbose_name="country",
        related_name="tenant_onboard_country",
        on_delete=models.PROTECT,
    )
    state = models.ForeignKey(
        State,
        verbose_name="state",
        related_name="tenant_onboard_state",
        on_delete=models.PROTECT,
    )
    district = models.ForeignKey(
        District,
        verbose_name="district",
        related_name="tenant_onboard_district",
        on_delete=models.PROTECT,
    )
    taluka = models.ForeignKey(
        Taluka,
        verbose_name="taluka",
        related_name="tenant_onboard_taluka",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    address = models.CharField(verbose_name="tenant_onboardaddress", max_length=500)

    pin_code = models.CharField(verbose_name="tenant_onboardpin_code", max_length=10)
    pan_no = models.CharField(verbose_name="tenant_onboardpan_no", max_length=15)
    tan_no = models.CharField(
        verbose_name="tenant_onboardtan_no", max_length=15, blank=True, null=True
    )
    gst_no = models.CharField(verbose_name="tenant_onboardgst_no", max_length=15)
    cin_no = models.CharField(
        verbose_name="tenant_onboardcin_no", max_length=21, blank=True, null=True
    )

    tenant_logo_path = models.CharField(
        verbose_name="tenant_onboardtenant_logo_path",
        max_length=255,
        blank=True,
        null=True,
    )
    password = models.CharField(
        max_length=128, blank=True, null=True, verbose_name='Password')
    plan_type_ref_id = models.ForeignKey(
        SubscriptionPlanMst,
        verbose_name="subscription_ref_id_tenant",
        related_name="subscription_ref_id_tenant",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    tenant_ref_id = models.ForeignKey(
        Tenant,
        verbose_name="tenant_ref_id",
        related_name="tenant_ref_id",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    class Meta:
        db_table = "tbl_tenant_onboard_temp"




class UserSubscription(BaseModel):
    plan_ref_id = models.ForeignKey(
        SubscriptionPlanMst,
        verbose_name="user_subscriptionmst_ref_id",
        related_name="user_subscriptionmst_ref_id",
        on_delete=models.CASCADE,
    )
    tenant_temp_ref_id =  models.ForeignKey(
        TenantOnboardTemp,
        verbose_name="tenant_temp_ref_id",
        related_name="tenant_temp_ref_id",
        on_delete=models.CASCADE,
    )
    tenant_id = models.ForeignKey(
        Tenant,
        verbose_name="tenant_temp_ref_id",
        related_name="tenant_temp_ref_id",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    subscription_start_date = models.DateField(verbose_name="Subscription Start Date",blank=True, null=True)
    subscription_end_date = models.DateField(verbose_name="Subscription End Date",blank=True, null=True)

    payment_id = models.CharField(max_length=255,verbose_name="Payment Id",blank=True)
    payment_status = models.CharField(max_length=30,verbose_name="Payment Status", default = 'Open')
    is_terms_and_conditions_accepted = models.BooleanField(default=False, verbose_name="is_terms_and_conditions_accepted")
    terms_and_conditions_accepted_date = models.DateField(verbose_name="terms_and_conditions_accepted_date", blank=True, null=True)
    image_path =  models.TextField(
        verbose_name="header_image_details", blank=True
    )
    transaction_date = models.DateField(verbose_name="transaction_date", blank=True, null=True)
    transaction_id = models.IntegerField(verbose_name="transaction_id", blank=True, null=True)
    transaction_type_id = models.IntegerField(verbose_name="transaction_type_id", blank=True, null=True)
    transaction_ref_no = models.CharField(
        max_length=255, verbose_name="transaction_ref_no", blank=True
    ) #invoice_ref_id
    subscription_charges = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Subscription Charges")
    base_currency_subscription_charges = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Base Currency Subscription Charges")
    cgst_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="CGST Amount")
    sgst_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="SGST Amount")
    igst_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="IGST Amount")
    total_tax_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Total Amount")
    base_currency_cgst_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Base Currency CGST Amount")
    base_currency_sgst_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Base Currency SGST Amount")
    base_currency_igst_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Base Currency IGST Amount")
    base_currency_total_tax_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Base Currency Total Amount")
    cgst_rate = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="CGST Rate")
    sgst_rate = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="SGST Rate")
    igst_rate = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="IGST Rate") 
    total_subscription_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Total Subscription Amount")
    base_currency_total_subscription_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Base Currency Total Subscription Amount")
    
    opening_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Opening Amount")
    transaction_amount = models.DecimalField(default=0,max_digits=15,decimal_places=4,verbose_name="Transaction Amount")
    class Meta:
        db_table = "tbl_user_subscription"