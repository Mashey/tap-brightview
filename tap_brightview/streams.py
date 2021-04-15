import singer
import sys
import tap_brightview.helpers as helper
from tap_brightview.client import HiveClient

LOGGER = singer.get_logger()


class Stream:
    table_name = ""
    tap_stream_id = None
    key_properties = []
    replication_method = ""
    valid_replication_keys = []
    replication_key = "last_commit_time"
    object_type = ""
    response_length = 10000
    offset = 0
    limit = 10000

    def __init__(self, state, config):
        self.state = state
        self.config = config

    def records_sync(self):
        stream_finished = False
        query_attempts = 1
        restart_count = 0
        json_schema = helper.open_json_schema(self.table_name)
        bookmark_value = singer.get_bookmark(
            self.state,
            self.tap_stream_id,
            self.replication_key,
            "1970-01-01 00:00:00.000000",
        )

        while stream_finished == False:
            try:
                client = HiveClient(self.config)
                while self.response_length >= self.limit:
                    record_count = 0
                    LOGGER.info(f"Sending Query: {query_attempts}")
                    for row in client.query_database(
                        json_schema,
                        self.table_name,
                        limit=self.limit,
                        offset=self.offset,
                        id=self.key_properties[0],
                        limit_key=self.replication_key,
                        limit_key_value=bookmark_value,
                    ):

                        record_count += 1
                        yield row

                    if self.offset == 0:
                        self.offset += 1

                    self.offset += self.limit
                    query_attempts += 1
                    self.response_length = record_count

                    if self.response_length < self.limit:
                        stream_finished = True
                        LOGGER.info(f"{self.table_name} sync completed.")
                        LOGGER.info(f"Creating bookmark for {self.tap_stream_id} stream")
                        client.sql.close()
                        client.client.close()

            except Exception as e:
                LOGGER.warning(f"Client error {e} :: Closing SQL and Connection.")
                LOGGER.info("Restarting Client")
                restart_count += 1
                singer.write_bookmark(
                    self.state, self.tap_stream_id, "restarts", restart_count
                )
                client = HiveClient(self.config)
                continue


class IncrementalStream(Stream):
    replication_method = "INCREMENTAL"


class FullTableStream(Stream):
    replication_method = "FULL_TABLE"


class Activity(IncrementalStream):
    table_name = "activity"
    tap_stream_id = "activity"
    key_properties = ["activity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityLog(IncrementalStream):
    table_name = "activity_log"
    tap_stream_id = "activity_log"
    key_properties = ["activity_log_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Address(IncrementalStream):
    table_name = "address"
    tap_stream_id = "address"
    key_properties = ["address_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActProcMatrixDsc(IncrementalStream):
    table_name = "act_proc_matrix_dsc"
    tap_stream_id = "act_proc_matrix_dsc"
    key_properties = ["act_proc_matrix_dsc_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityDetail(IncrementalStream):
    table_name = "activity_detail"
    tap_stream_id = "activity_detail"
    key_properties = ["activity_detail_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityDetailDsc(IncrementalStream):
    table_name = "activity_detail_dsc"
    tap_stream_id = "activity_detail_dsc"
    key_properties = ["activity_detail_dsc_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityDsc(IncrementalStream):
    table_name = "activity_dsc"
    tap_stream_id = "activity_dsc"
    key_properties = ["activity_dsc_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityError(IncrementalStream):
    table_name = "activity_error"
    tap_stream_id = "activity_error"
    key_properties = ["activity_error_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityProcedureAddon(IncrementalStream):
    table_name = "activity_procedure_addon"
    tap_stream_id = "activity_procedure_addon"
    key_properties = ["activity_procedure_addon_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityProcedureClm(IncrementalStream):
    table_name = "activity_procedure_clm"
    tap_stream_id = "activity_procedure_clm"
    key_properties = ["activity_procedure_clm_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityProcedureClmMod(IncrementalStream):
    table_name = "activity_procedure_clm_mod"
    tap_stream_id = "activity_procedure_clm_mod"
    key_properties = ["activity_procedure_clm_mod_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityProcedureMatrix(IncrementalStream):
    table_name = "activity_procedure_matrix"
    tap_stream_id = "activity_procedure_matrix"
    key_properties = ["activity_procedure_matrix_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ActivityProgramMatrix(IncrementalStream):
    table_name = "activity_program_matrix"
    tap_stream_id = "activity_program_matrix"
    key_properties = ["activity_program_matrix_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Addendum(IncrementalStream):
    table_name = "addendum"
    tap_stream_id = "addendum"
    key_properties = ["addendum_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AdminCoPay(IncrementalStream):
    table_name = "admin_co_pay"
    tap_stream_id = "admin_co_pay"
    key_properties = ["admin_co_pay_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AdminCoPayMatrix(IncrementalStream):
    table_name = "admin_co_pay_matrix"
    tap_stream_id = "admin_co_pay_matrix"
    key_properties = ["admin_co_pay_matrix_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AdminCoPayMatrixLic(IncrementalStream):
    table_name = "admin_co_pay_matrix_lic"
    tap_stream_id = "admin_co_pay_matrix_lic"
    key_properties = ["admin_co_pay_matrix_lic_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AdminGroup(IncrementalStream):
    table_name = "admin_group"
    tap_stream_id = "admin_group"
    key_properties = ["admin_group_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AdminOrderStatus(IncrementalStream):
    table_name = "admin_order_status"
    tap_stream_id = "admin_order_status"
    key_properties = ["admin_order_status_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Alert(IncrementalStream):
    table_name = "alert"
    tap_stream_id = "alert"
    key_properties = ["alert_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AllergyEntry(IncrementalStream):
    table_name = "allergy_entry"
    tap_stream_id = "allergy_entry"
    key_properties = ["allergy_entry_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AuditDataedit(IncrementalStream):
    table_name = "audit_dataedit"
    tap_stream_id = "audit_dataedit"
    key_properties = ["audit_dataedit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AuditDeleteValues(IncrementalStream):
    table_name = "audit_delete_values"
    tap_stream_id = "audit_delete_values"
    key_properties = ["audit_delete_values_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AuditLog(IncrementalStream):
    table_name = "audit_log"
    tap_stream_id = "audit_log"
    key_properties = ["audit_log_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AuditPageTitle(IncrementalStream):
    table_name = "audit_page_title"
    tap_stream_id = "audit_page_title"
    key_properties = ["audit_page_title_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class AuditRowDelete(IncrementalStream):
    table_name = "audit_row_delete"
    tap_stream_id = "audit_row_delete"
    key_properties = ["audit_row_delete_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CashSheet(IncrementalStream):
    table_name = "cash_sheet"
    tap_stream_id = "cash_sheet"
    key_properties = ["cash_sheet_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CashSheetLine(IncrementalStream):
    table_name = "cash_sheet_line"
    tap_stream_id = "cash_sheet_line"
    key_properties = ["cash_sheet_line_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CfData(IncrementalStream):
    table_name = "cf_data"
    tap_stream_id = "cf_data"
    key_properties = ["cf_edit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["created_date"]
    replication_key = "created_date"


class CfDataHist(IncrementalStream):
    table_name = "cf_data_hist"
    tap_stream_id = "cf_data_hist"
    key_properties = ["cf_edit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["created_date"]
    replication_key = "created_date"


class Claim(IncrementalStream):
    table_name = "claim"
    tap_stream_id = "claim"
    key_properties = ["claim_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimBatch(IncrementalStream):
    table_name = "claim_batch"
    tap_stream_id = "claim_batch"
    key_properties = ["claim_batch_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimBatchLine(IncrementalStream):
    table_name = "claim_batch_line"
    tap_stream_id = "claim_batch_line"
    key_properties = ["claim_batch_line_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimBillNext(IncrementalStream):
    table_name = "claim_bill_next"
    tap_stream_id = "claim_bill_next"
    key_properties = ["claim_bill_next_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimBillNextItem(IncrementalStream):
    table_name = "claim_bill_next_item"
    tap_stream_id = "claim_bill_next_item"
    key_properties = ["claim_bill_next_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimDiag(IncrementalStream):
    table_name = "claim_diag"
    tap_stream_id = "claim_diag"
    key_properties = ["claim_diag_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimEngineRun(IncrementalStream):
    table_name = "claim_engine_run"
    tap_stream_id = "claim_engine_run"
    key_properties = ["claim_engine_run_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimError(IncrementalStream):
    table_name = "claim_error"
    tap_stream_id = "claim_error"
    key_properties = ["claim_error_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimFollowupComment(IncrementalStream):
    table_name = "claim_followup_comment"
    tap_stream_id = "claim_followup_comment"
    key_properties = ["claim_followup_comment_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimItem(IncrementalStream):
    table_name = "claim_item"
    tap_stream_id = "claim_item"
    key_properties = ["claim_item_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimItemActivity(IncrementalStream):
    table_name = "claim_item_activity"
    tap_stream_id = "claim_item_activity"
    key_properties = ["claim_item_activity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimItemEditAudit(IncrementalStream):
    table_name = "claim_item_edit_audit"
    tap_stream_id = "claim_item_edit_audit"
    key_properties = ["claim_item_edit_audit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimItemLine(IncrementalStream):
    table_name = "claim_item_line"
    tap_stream_id = "claim_item_line"
    key_properties = ["claim_item_line_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimItemModifier(IncrementalStream):
    table_name = "claim_item_modifier"
    tap_stream_id = "claim_item_modifier"
    key_properties = ["claim_item_modifier_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimNote(IncrementalStream):
    table_name = "claim_note"
    tap_stream_id = "claim_note"
    key_properties = ["claim_note_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimRollup(IncrementalStream):
    table_name = "claim_rollup"
    tap_stream_id = "claim_rollup"
    key_properties = ["claim_rollup_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClaimValueCode(IncrementalStream):
    table_name = "claim_value_code"
    tap_stream_id = "claim_value_code"
    key_properties = ["claim_value_code_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Client(IncrementalStream):
    table_name = "client"
    tap_stream_id = "client"
    key_properties = ["client_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientAllergy(IncrementalStream):
    table_name = "client_allergy"
    tap_stream_id = "client_allergy"
    key_properties = ["client_allergy_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientAuthProcModif(IncrementalStream):
    table_name = "client_auth_proc_modif"
    tap_stream_id = "client_auth_proc_modif"
    key_properties = ["client_auth_proc_modif_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientAuthProcedure(IncrementalStream):
    table_name = "client_auth_procedure"
    tap_stream_id = "client_auth_procedure"
    key_properties = ["client_auth_procedure_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientBalance(IncrementalStream):
    table_name = "client_balance"
    tap_stream_id = "client_balance"
    key_properties = ["client_balance_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientBlackBox(IncrementalStream):
    table_name = "client_black_box"
    tap_stream_id = "client_black_box"
    key_properties = ["client_black_box_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientBlackBoxStaff(IncrementalStream):
    table_name = "client_black_box_staff"
    tap_stream_id = "client_black_box_staff"
    key_properties = ["client_black_box_staff_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientCoPay(IncrementalStream):
    table_name = "client_co_pay"
    tap_stream_id = "client_co_pay"
    key_properties = ["client_co_pay_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientCoPayMatrix(IncrementalStream):
    table_name = "client_co_pay_matrix"
    tap_stream_id = "client_co_pay_matrix"
    key_properties = ["client_co_pay_matrix_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientCoPayMatrixLic(IncrementalStream):
    table_name = "client_co_pay_matrix_lic"
    tap_stream_id = "client_co_pay_matrix_lic"
    key_properties = ["client_co_pay_matrix_lic_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientConsent(IncrementalStream):
    table_name = "client_consent"
    tap_stream_id = "client_consent"
    key_properties = ["client_consent_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientEpisode(IncrementalStream):
    table_name = "client_episode"
    tap_stream_id = "client_episode"
    key_properties = ["client_episode_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientEpisodeOrgMap(IncrementalStream):
    table_name = "client_episode_org_map"
    tap_stream_id = "client_episode_org_map"
    key_properties = ["client_episode_org_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientEpisodePrefs(IncrementalStream):
    table_name = "client_episode_prefs"
    tap_stream_id = "client_episode_prefs"
    key_properties = ["client_episode_prefs_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientEpisodeTriag(IncrementalStream):
    table_name = "client_episode_triag"
    tap_stream_id = "client_episode_triag"
    key_properties = ["client_episode_triag_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientGroup(IncrementalStream):
    table_name = "client_group"
    tap_stream_id = "client_group"
    key_properties = ["client_group_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientGuarantor(IncrementalStream):
    table_name = "client_guarantor"
    tap_stream_id = "client_guarantor"
    key_properties = ["client_guarantor_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientGuarantorMix(IncrementalStream):
    table_name = "client_guarantor_mix"
    tap_stream_id = "client_guarantor_mix"
    key_properties = ["client_guarantor_mix_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientLiability(IncrementalStream):
    table_name = "client_liability"
    tap_stream_id = "client_liability"
    key_properties = ["client_liability_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientLiabilityMem(IncrementalStream):
    table_name = "client_liability_mem"
    tap_stream_id = "client_liability_mem"
    key_properties = ["client_liability_mem_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientLiabilityMemExp(IncrementalStream):
    table_name = "client_liability_mem_exp"
    tap_stream_id = "client_liability_mem_exp"
    key_properties = ["client_liability_mem_exp_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientMedication(IncrementalStream):
    table_name = "client_medication"
    tap_stream_id = "client_medication"
    key_properties = ["client_medication_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientMessage(IncrementalStream):
    table_name = "client_message"
    tap_stream_id = "client_message"
    key_properties = ["client_message_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientPayerAuth(IncrementalStream):
    table_name = "client_payer_auth"
    tap_stream_id = "client_payer_auth"
    key_properties = ["client_payer_auth_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientPayerPlan(IncrementalStream):
    table_name = "client_payer_plan"
    tap_stream_id = "client_payer_plan"
    key_properties = ["client_payer_plan_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientPayerPlanDate(IncrementalStream):
    table_name = "client_payer_plan_date"
    tap_stream_id = "client_payer_plan_date"
    key_properties = ["client_payer_plan_date_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientPcp(IncrementalStream):
    table_name = "client_pcp"
    tap_stream_id = "client_pcp"
    key_properties = ["client_pcp_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientPharmacy(IncrementalStream):
    table_name = "client_pharmacy"
    tap_stream_id = "client_pharmacy"
    key_properties = ["client_pharmacy_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientProgram(IncrementalStream):
    table_name = "client_program"
    tap_stream_id = "client_program"
    key_properties = ["client_program_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientProgramCode(IncrementalStream):
    table_name = "client_program_code"
    tap_stream_id = "client_program_code"
    key_properties = ["client_program_code_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientProgramDate(IncrementalStream):
    table_name = "client_program_date"
    tap_stream_id = "client_program_date"
    key_properties = ["client_program_date_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientProgramUnbillable(IncrementalStream):
    table_name = "client_program_unbillable"
    tap_stream_id = "client_program_unbillable"
    key_properties = ["client_program_unbillable_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientProvider(IncrementalStream):
    table_name = "client_provider"
    tap_stream_id = "client_provider"
    key_properties = ["client_provider_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientRecordInv(IncrementalStream):
    table_name = "client_record_inv"
    tap_stream_id = "client_record_inv"
    key_properties = ["client_record_inv_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientRecordInvChange(IncrementalStream):
    table_name = "client_record_inv_change"
    tap_stream_id = "client_record_inv_change"
    key_properties = ["client_record_inv_change_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientRelationship(IncrementalStream):
    table_name = "client_relationship"
    tap_stream_id = "client_relationship"
    key_properties = ["client_relationship_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientScannedDocument(IncrementalStream):
    table_name = "client_scanned_document"
    tap_stream_id = "client_scanned_document"
    key_properties = ["client_scanned_document_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientSlidingScale(IncrementalStream):
    table_name = "client_sliding_scale"
    tap_stream_id = "client_sliding_scale"
    key_properties = ["client_sliding_scale_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientStaff(IncrementalStream):
    table_name = "client_staff"
    tap_stream_id = "client_staff"
    key_properties = ["client_staff_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientView(IncrementalStream):
    table_name = "client_view"
    tap_stream_id = "client_view"
    key_properties = ["client_view_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClientViewAttempt(IncrementalStream):
    table_name = "client_view_attempt"
    tap_stream_id = "client_view_attempt"
    key_properties = ["client_view_attempt_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClinicalRecon(IncrementalStream):
    table_name = "clinical_recon"
    tap_stream_id = "clinical_recon"
    key_properties = ["clinical_recon_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClinicianAllergyEntry(IncrementalStream):
    table_name = "clinician_allergy_entry"
    tap_stream_id = "clinician_allergy_entry"
    key_properties = ["clinician_allergy_entry_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClinicianOrdMedication(IncrementalStream):
    table_name = "clinician_ord_medication"
    tap_stream_id = "clinician_ord_medication"
    key_properties = ["clinician_ord_medication_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ClinicianUser(IncrementalStream):
    table_name = "clinician_user"
    tap_stream_id = "clinician_user"
    key_properties = ["clinician_user_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CodeSystem(IncrementalStream):
    table_name = "code_system"
    tap_stream_id = "code_system"
    key_properties = ["code_system_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CollectionAssignment(IncrementalStream):
    table_name = "collection_assignment"
    tap_stream_id = "collection_assignment"
    key_properties = ["collection_assignment_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CollectionAssignmentClms(IncrementalStream):
    table_name = "collection_assignment_clms"
    tap_stream_id = "collection_assignment_clms"
    key_properties = ["collection_assignment_clms_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CsBatch(IncrementalStream):
    table_name = "cs_batch"
    tap_stream_id = "cs_batch"
    key_properties = ["cs_batch_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CsBatchClient(IncrementalStream):
    table_name = "cs_batch_client"
    tap_stream_id = "cs_batch_client"
    key_properties = ["cs_batch_client_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CsBatchClientAging(IncrementalStream):
    table_name = "cs_batch_client_aging"
    tap_stream_id = "cs_batch_client_aging"
    key_properties = ["cs_batch_client_aging_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CsBatchClientClaim(IncrementalStream):
    table_name = "cs_batch_client_claim"
    tap_stream_id = "cs_batch_client_claim"
    key_properties = ["cs_batch_client_claim_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class CsBatchClientClaimTran(IncrementalStream):
    table_name = "cs_batch_client_claim_tran"
    tap_stream_id = "cs_batch_client_claim_tran"
    key_properties = ["cs_batch_client_claim_tran_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Deposit(IncrementalStream):
    table_name = "deposit"
    tap_stream_id = "deposit"
    key_properties = ["deposit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DepositActivity(IncrementalStream):
    table_name = "deposit_activity"
    tap_stream_id = "deposit_activity"
    key_properties = ["deposit_activity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DepositAudit(IncrementalStream):
    table_name = "deposit_audit"
    tap_stream_id = "deposit_audit"
    key_properties = ["deposit_audit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Descriptor(IncrementalStream):
    table_name = "descriptor"
    tap_stream_id = "descriptor"
    key_properties = ["descriptor_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DescriptorMappedValue(IncrementalStream):
    table_name = "descriptor_mapped_value"
    tap_stream_id = "descriptor_mapped_value"
    key_properties = ["descriptor_mapped_value_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Document(IncrementalStream):
    table_name = "document"
    tap_stream_id = "document"
    key_properties = ["document_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DocumentAudit(IncrementalStream):
    table_name = "document_audit"
    tap_stream_id = "document_audit"
    key_properties = ["document_audit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DocumentGrouping(IncrementalStream):
    table_name = "document_grouping"
    tap_stream_id = "document_grouping"
    key_properties = ["document_grouping_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DocumentSignature(IncrementalStream):
    table_name = "document_signature"
    tap_stream_id = "document_signature"
    key_properties = ["document_signature_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DocumentSignaturePad(IncrementalStream):
    table_name = "document_signature_pad"
    tap_stream_id = "document_signature_pad"
    key_properties = ["document_signature_pad_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DocumentStatus(IncrementalStream):
    table_name = "document_status"
    tap_stream_id = "document_status"
    key_properties = ["document_status_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DsmDiagCategory(IncrementalStream):
    table_name = "dsm_diag_category"
    tap_stream_id = "dsm_diag_category"
    key_properties = ["dsm_diag_category_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DsmDiagCategoryRange(IncrementalStream):
    table_name = "dsm_diag_category_range"
    tap_stream_id = "dsm_diag_category_range"
    key_properties = ["dsm_diag_category_range_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DsmDiagnosis(IncrementalStream):
    table_name = "dsm_diagnosis"
    tap_stream_id = "dsm_diagnosis"
    key_properties = ["dsm_diagnosis_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class DynHcfa(IncrementalStream):
    table_name = "dyn_hcfa"
    tap_stream_id = "dyn_hcfa"
    key_properties = ["dyn_hcfa_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi270Batch(IncrementalStream):
    table_name = "edi_270_batch"
    tap_stream_id = "edi_270_batch"
    key_properties = ["edi_270_batch_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi270Detail(IncrementalStream):
    table_name = "edi_270_detail"
    tap_stream_id = "edi_270_detail"
    key_properties = ["edi_270_detail_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi271(IncrementalStream):
    table_name = "edi_271"
    tap_stream_id = "edi_271"
    key_properties = ["edi_271_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi271EbDates(IncrementalStream):
    table_name = "edi_271_eb_dates"
    tap_stream_id = "edi_271_eb_dates"
    key_properties = ["edi_271_eb_dates_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi271Eligible(IncrementalStream):
    table_name = "edi_271_eligible"
    tap_stream_id = "edi_271_eligible"
    key_properties = ["edi_271_eligible_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi271Reference(IncrementalStream):
    table_name = "edi_271_reference"
    tap_stream_id = "edi_271_reference"
    key_properties = ["edi_271_reference_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi271RequestVal(IncrementalStream):
    table_name = "edi_271_request_val"
    tap_stream_id = "edi_271_request_val"
    key_properties = ["edi_271_request_val_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi271Subscriber(IncrementalStream):
    table_name = "edi_271_subscriber"
    tap_stream_id = "edi_271_subscriber"
    key_properties = ["edi_271_subscriber_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi271SubscriberBenefit(IncrementalStream):
    table_name = "edi_271_subscriber_benefit"
    tap_stream_id = "edi_271_subscriber_benefit"
    key_properties = ["edi_271_subscriber_benefit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835(IncrementalStream):
    table_name = "edi_835"
    tap_stream_id = "edi_835"
    key_properties = ["edi_835_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835AdjOrg(IncrementalStream):
    table_name = "edi_835_adj_org"
    tap_stream_id = "edi_835_adj_org"
    key_properties = ["edi_835_adj_org_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835AdjOrgMatrix(IncrementalStream):
    table_name = "edi_835_adj_org_matrix"
    tap_stream_id = "edi_835_adj_org_matrix"
    key_properties = ["edi_835_adj_org_matrix_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835AdjOrgPayerPlan(IncrementalStream):
    table_name = "edi_835_adj_org_payer_plan"
    tap_stream_id = "edi_835_adj_org_payer_plan"
    key_properties = ["edi_835_adj_org_payer_plan_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835Adjustment(IncrementalStream):
    table_name = "edi_835_adjustment"
    tap_stream_id = "edi_835_adjustment"
    key_properties = ["edi_835_adjustment_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835AdjustmentReason(IncrementalStream):
    table_name = "edi_835_adjustment_reason"
    tap_stream_id = "edi_835_adjustment_reason"
    key_properties = ["edi_835_adjustment_reason_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835Plb(IncrementalStream):
    table_name = "edi_835_plb"
    tap_stream_id = "edi_835_plb"
    key_properties = ["edi_835_plb_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835Reference(IncrementalStream):
    table_name = "edi_835_reference"
    tap_stream_id = "edi_835_reference"
    key_properties = ["edi_835_reference_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835Service(IncrementalStream):
    table_name = "edi_835_service"
    tap_stream_id = "edi_835_service"
    key_properties = ["edi_835_service_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi835Transaction(IncrementalStream):
    table_name = "edi_835_transaction"
    tap_stream_id = "edi_835_transaction"
    key_properties = ["edi_835_transaction_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi837(IncrementalStream):
    table_name = "edi_837"
    tap_stream_id = "edi_837"
    key_properties = ["edi_837_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi837Element(IncrementalStream):
    table_name = "edi_837_element"
    tap_stream_id = "edi_837_element"
    key_properties = ["edi_837_element_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Edi837Level(IncrementalStream):
    table_name = "edi_837_level"
    tap_stream_id = "edi_837_level"
    key_properties = ["edi_837_level_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class EdiCode(IncrementalStream):
    table_name = "edi_code"
    tap_stream_id = "edi_code"
    key_properties = ["edi_code_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class EdiType(IncrementalStream):
    table_name = "edi_type"
    tap_stream_id = "edi_type"
    key_properties = ["edi_type_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class EpisodeType(IncrementalStream):
    table_name = "episode_type"
    tap_stream_id = "episode_type"
    key_properties = ["episode_type_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Error(IncrementalStream):
    table_name = "error"
    tap_stream_id = "error"
    key_properties = ["error_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxAllergy(IncrementalStream):
    table_name = "erx_allergy"
    tap_stream_id = "erx_allergy"
    key_properties = ["erx_allergy_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxClient(IncrementalStream):
    table_name = "erx_client"
    tap_stream_id = "erx_client"
    key_properties = ["erx_client_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxDrug(IncrementalStream):
    table_name = "erx_drug"
    tap_stream_id = "erx_drug"
    key_properties = ["erx_drug_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxMedication(IncrementalStream):
    table_name = "erx_medication"
    tap_stream_id = "erx_medication"
    key_properties = ["erx_medication_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxNotification(IncrementalStream):
    table_name = "erx_notification"
    tap_stream_id = "erx_notification"
    key_properties = ["erx_notification_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxPharmacy(IncrementalStream):
    table_name = "erx_pharmacy"
    tap_stream_id = "erx_pharmacy"
    key_properties = ["erx_pharmacy_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxPrescription(IncrementalStream):
    table_name = "erx_prescription"
    tap_stream_id = "erx_prescription"
    key_properties = ["erx_prescription_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxPrescriptionStatus(IncrementalStream):
    table_name = "erx_prescription_status"
    tap_stream_id = "erx_prescription_status"
    key_properties = ["erx_prescription_status_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ErxSig(IncrementalStream):
    table_name = "erx_sig"
    tap_stream_id = "erx_sig"
    key_properties = ["erx_sig_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class FailedLogin(IncrementalStream):
    table_name = "failed_login"
    tap_stream_id = "failed_login"
    key_properties = ["failed_login_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class FfsBatch(IncrementalStream):
    table_name = "ffs_batch"
    tap_stream_id = "ffs_batch"
    key_properties = ["ffs_batch_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class FfsBatchLine(IncrementalStream):
    table_name = "ffs_batch_line"
    tap_stream_id = "ffs_batch_line"
    key_properties = ["ffs_batch_line_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class FfsBatchLineErr(IncrementalStream):
    table_name = "ffs_batch_line_err"
    tap_stream_id = "ffs_batch_line_err"
    key_properties = ["ffs_batch_line_err_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class FfsBatchLineHx(IncrementalStream):
    table_name = "ffs_batch_line_hx"
    tap_stream_id = "ffs_batch_line_hx"
    key_properties = ["ffs_batch_line_hx_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodeActivity(IncrementalStream):
    table_name = "gl_code_activity"
    tap_stream_id = "gl_code_activity"
    key_properties = ["gl_code_activity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodeDate(IncrementalStream):
    table_name = "gl_code_date"
    tap_stream_id = "gl_code_date"
    key_properties = ["gl_code_date_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodeOrgProg(IncrementalStream):
    table_name = "gl_code_org_prog"
    tap_stream_id = "gl_code_org_prog"
    key_properties = ["gl_code_org_prog_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodeOrganization(IncrementalStream):
    table_name = "gl_code_organization"
    tap_stream_id = "gl_code_organization"
    key_properties = ["gl_code_organization_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodePayer(IncrementalStream):
    table_name = "gl_code_payer"
    tap_stream_id = "gl_code_payer"
    key_properties = ["gl_code_payer_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodePopulation(IncrementalStream):
    table_name = "gl_code_population"
    tap_stream_id = "gl_code_population"
    key_properties = ["gl_code_population_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodeProgAct(IncrementalStream):
    table_name = "gl_code_prog_act"
    tap_stream_id = "gl_code_prog_act"
    key_properties = ["gl_code_prog_act_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlCodeProgram(IncrementalStream):
    table_name = "gl_code_program"
    tap_stream_id = "gl_code_program"
    key_properties = ["gl_code_program_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlDetail(IncrementalStream):
    table_name = "gl_detail"
    tap_stream_id = "gl_detail"
    key_properties = ["gl_detail_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlError(IncrementalStream):
    table_name = "gl_error"
    tap_stream_id = "gl_error"
    key_properties = ["gl_error_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class GlMap(IncrementalStream):
    table_name = "gl_map"
    tap_stream_id = "gl_map"
    key_properties = ["gl_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Guarantor(IncrementalStream):
    table_name = "guarantor"
    tap_stream_id = "guarantor"
    key_properties = ["guarantor_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class IntakeFollowup(IncrementalStream):
    table_name = "intake_followup"
    tap_stream_id = "intake_followup"
    key_properties = ["intake_followup_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class IntakeTracking(IncrementalStream):
    table_name = "intake_tracking"
    tap_stream_id = "intake_tracking"
    key_properties = ["intake_tracking_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class IpLog(IncrementalStream):
    table_name = "ip_log"
    tap_stream_id = "ip_log"
    key_properties = ["ip_log_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Licensure(IncrementalStream):
    table_name = "licensure"
    tap_stream_id = "licensure"
    key_properties = ["licensure_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Location(IncrementalStream):
    table_name = "location"
    tap_stream_id = "location"
    key_properties = ["location_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MacsisAdmDis(IncrementalStream):
    table_name = "macsis_adm_dis"
    tap_stream_id = "macsis_adm_dis"
    key_properties = ["macsis_adm_dis_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MacsisAdmDisData(IncrementalStream):
    table_name = "macsis_adm_dis_data"
    tap_stream_id = "macsis_adm_dis_data"
    key_properties = ["macsis_adm_dis_data_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MacsisClientSigPad(IncrementalStream):
    table_name = "macsis_client_sig_pad"
    tap_stream_id = "macsis_client_sig_pad"
    key_properties = ["macsis_client_sig_pad_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MacsisEnrollmentForm(IncrementalStream):
    table_name = "macsis_enrollment_form"
    tap_stream_id = "macsis_enrollment_form"
    key_properties = ["macsis_enrollment_form_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MacsisEnrollmentFormD(IncrementalStream):
    table_name = "macsis_enrollment_form_d"
    tap_stream_id = "macsis_enrollment_form_d"
    key_properties = ["macsis_enrollment_form_d_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MacsisEnrollmentVerify(IncrementalStream):
    table_name = "macsis_enrollment_verify"
    tap_stream_id = "macsis_enrollment_verify"
    key_properties = ["macsis_enrollment_verify_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MasterModifier(IncrementalStream):
    table_name = "master_modifier"
    tap_stream_id = "master_modifier"
    key_properties = ["master_modifier_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MasterModifierDetail(IncrementalStream):
    table_name = "master_modifier_detail"
    tap_stream_id = "master_modifier_detail"
    key_properties = ["master_modifier_detail_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MasterModifierOrgMap(IncrementalStream):
    table_name = "master_modifier_org_map"
    tap_stream_id = "master_modifier_org_map"
    key_properties = ["master_modifier_org_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MasterPersonIndex(IncrementalStream):
    table_name = "master_person_index"
    tap_stream_id = "master_person_index"
    key_properties = ["master_person_index_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Measure(IncrementalStream):
    table_name = "measure"
    tap_stream_id = "measure"
    key_properties = ["measure_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MeasureQuestion(IncrementalStream):
    table_name = "measure_question"
    tap_stream_id = "measure_question"
    key_properties = ["measure_question_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MeasureQuestionVal(IncrementalStream):
    table_name = "measure_question_val"
    tap_stream_id = "measure_question_val"
    key_properties = ["measure_question_val_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MeasureSection(IncrementalStream):
    table_name = "measure_section"
    tap_stream_id = "measure_section"
    key_properties = ["measure_section_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MeasureSubtotal(IncrementalStream):
    table_name = "measure_subtotal"
    tap_stream_id = "measure_subtotal"
    key_properties = ["measure_subtotal_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Medication(IncrementalStream):
    table_name = "medication"
    tap_stream_id = "medication"
    key_properties = ["medication_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MedicationDispense(IncrementalStream):
    table_name = "medication_dispense"
    tap_stream_id = "medication_dispense"
    key_properties = ["medication_dispense_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MedicationEntry(IncrementalStream):
    table_name = "medication_entry"
    tap_stream_id = "medication_entry"
    key_properties = ["medication_entry_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MedicationOrgMap(IncrementalStream):
    table_name = "medication_org_map"
    tap_stream_id = "medication_org_map"
    key_properties = ["medication_org_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Menu(IncrementalStream):
    table_name = "menu"
    tap_stream_id = "menu"
    key_properties = ["menu_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MenuOrgMap(IncrementalStream):
    table_name = "menu_org_map"
    tap_stream_id = "menu_org_map"
    key_properties = ["menu_org_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MenuPriv(IncrementalStream):
    table_name = "menu_priv"
    tap_stream_id = "menu_priv"
    key_properties = ["menu_priv_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MenuSystem(IncrementalStream):
    table_name = "menu_system"
    tap_stream_id = "menu_system"
    key_properties = ["menu_system_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MenuSystemOrgMap(IncrementalStream):
    table_name = "menu_system_org_map"
    tap_stream_id = "menu_system_org_map"
    key_properties = ["menu_system_org_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModCallLog(IncrementalStream):
    table_name = "mod_call_log"
    tap_stream_id = "mod_call_log"
    key_properties = ["mod_call_log_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModEmploymt(IncrementalStream):
    table_name = "mod_employmt"
    tap_stream_id = "mod_employmt"
    key_properties = ["mod_employmt_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModEvalManagement(IncrementalStream):
    table_name = "mod_eval_management"
    tap_stream_id = "mod_eval_management"
    key_properties = ["mod_eval_management_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModGoalsAddrSummary(IncrementalStream):
    table_name = "mod_goals_addr_summary"
    tap_stream_id = "mod_goals_addr_summary"
    key_properties = ["mod_goals_addr_summary_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModLabResult(IncrementalStream):
    table_name = "mod_lab_result"
    tap_stream_id = "mod_lab_result"
    key_properties = ["mod_lab_result_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModLabResultDtl(IncrementalStream):
    table_name = "mod_lab_result_dtl"
    tap_stream_id = "mod_lab_result_dtl"
    key_properties = ["mod_lab_result_dtl_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModLegal(IncrementalStream):
    table_name = "mod_legal"
    tap_stream_id = "mod_legal"
    key_properties = ["mod_legal_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModLivingEd(IncrementalStream):
    table_name = "mod_living_ed"
    tap_stream_id = "mod_living_ed"
    key_properties = ["mod_living_ed_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModManualMedRec(IncrementalStream):
    table_name = "mod_manual_med_rec"
    tap_stream_id = "mod_manual_med_rec"
    key_properties = ["mod_manual_med_rec_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModMedDiagCat(IncrementalStream):
    table_name = "mod_med_diag_cat"
    tap_stream_id = "mod_med_diag_cat"
    key_properties = ["mod_med_diag_cat_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModMedication(IncrementalStream):
    table_name = "mod_medication"
    tap_stream_id = "mod_medication"
    key_properties = ["mod_medication_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModMemoNote(IncrementalStream):
    table_name = "mod_memo_note"
    tap_stream_id = "mod_memo_note"
    key_properties = ["mod_memo_note_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModPcpSignature(IncrementalStream):
    table_name = "mod_pcp_signature"
    tap_stream_id = "mod_pcp_signature"
    key_properties = ["mod_pcp_signature_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModPcpSignatureCbx(IncrementalStream):
    table_name = "mod_pcp_signature_cbx"
    tap_stream_id = "mod_pcp_signature_cbx"
    key_properties = ["mod_pcp_signature_cbx_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModReferral(IncrementalStream):
    table_name = "mod_referral"
    tap_stream_id = "mod_referral"
    key_properties = ["mod_referral_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModServiceAddition(IncrementalStream):
    table_name = "mod_service_addition"
    tap_stream_id = "mod_service_addition"
    key_properties = ["mod_service_addition_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModServiceDetail(IncrementalStream):
    table_name = "mod_service_detail"
    tap_stream_id = "mod_service_detail"
    key_properties = ["mod_service_detail_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModServiceDetailSb(IncrementalStream):
    table_name = "mod_service_detail_sb"
    tap_stream_id = "mod_service_detail_sb"
    key_properties = ["mod_service_detail_sb_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModSubAbuseDtlDsc(IncrementalStream):
    table_name = "mod_sub_abuse_dtl_dsc"
    tap_stream_id = "mod_sub_abuse_dtl_dsc"
    key_properties = ["mod_sub_abuse_dtl_dsc_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModSubstanceAbuse(IncrementalStream):
    table_name = "mod_substance_abuse"
    tap_stream_id = "mod_substance_abuse"
    key_properties = ["mod_substance_abuse_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModSubstanceAbuseDate(IncrementalStream):
    table_name = "mod_substance_abuse_date"
    tap_stream_id = "mod_substance_abuse_date"
    key_properties = ["mod_substance_abuse_date_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModSubstanceAbuseDsc(IncrementalStream):
    table_name = "mod_substance_abuse_dsc"
    tap_stream_id = "mod_substance_abuse_dsc"
    key_properties = ["mod_substance_abuse_dsc_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModSubstanceAbuseDtl(IncrementalStream):
    table_name = "mod_substance_abuse_dtl"
    tap_stream_id = "mod_substance_abuse_dtl"
    key_properties = ["mod_substance_abuse_dtl_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTedsNoms(IncrementalStream):
    table_name = "mod_teds_noms"
    tap_stream_id = "mod_teds_noms"
    key_properties = ["mod_teds_noms_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTobacco(IncrementalStream):
    table_name = "mod_tobacco"
    tap_stream_id = "mod_tobacco"
    key_properties = ["mod_tobacco_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTplanEntity(IncrementalStream):
    table_name = "mod_tplan_entity"
    tap_stream_id = "mod_tplan_entity"
    key_properties = ["mod_tplan_entity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTplanEntityDtl(IncrementalStream):
    table_name = "mod_tplan_entity_dtl"
    tap_stream_id = "mod_tplan_entity_dtl"
    key_properties = ["mod_tplan_entity_dtl_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTplanEntityMap(IncrementalStream):
    table_name = "mod_tplan_entity_map"
    tap_stream_id = "mod_tplan_entity_map"
    key_properties = ["mod_tplan_entity_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTplanMaster(IncrementalStream):
    table_name = "mod_tplan_master"
    tap_stream_id = "mod_tplan_master"
    key_properties = ["mod_tplan_master_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTransDischarge(IncrementalStream):
    table_name = "mod_trans_discharge"
    tap_stream_id = "mod_trans_discharge"
    key_properties = ["mod_trans_discharge_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDiag(IncrementalStream):
    table_name = "mod_tx_diag"
    tap_stream_id = "mod_tx_diag"
    key_properties = ["mod_tx_diag_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDiagAxis(IncrementalStream):
    table_name = "mod_tx_diag_axis"
    tap_stream_id = "mod_tx_diag_axis"
    key_properties = ["mod_tx_diag_axis_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDx(IncrementalStream):
    table_name = "mod_tx_dx"
    tap_stream_id = "mod_tx_dx"
    key_properties = ["mod_tx_dx_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDxCode(IncrementalStream):
    table_name = "mod_tx_dx_code"
    tap_stream_id = "mod_tx_dx_code"
    key_properties = ["mod_tx_dx_code_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDxCodeSpecSev(IncrementalStream):
    table_name = "mod_tx_dx_code_spec_sev"
    tap_stream_id = "mod_tx_dx_code_spec_sev"
    key_properties = ["mod_tx_dx_code_spec_sev_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDxDiag(IncrementalStream):
    table_name = "mod_tx_dx_diag"
    tap_stream_id = "mod_tx_dx_diag"
    key_properties = ["mod_tx_dx_diag_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDxDiagSpecSev(IncrementalStream):
    table_name = "mod_tx_dx_diag_spec_sev"
    tap_stream_id = "mod_tx_dx_diag_spec_sev"
    key_properties = ["mod_tx_dx_diag_spec_sev_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxDxInfo(IncrementalStream):
    table_name = "mod_tx_dx_info"
    tap_stream_id = "mod_tx_dx_info"
    key_properties = ["mod_tx_dx_info_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlan(IncrementalStream):
    table_name = "mod_tx_plan"
    tap_stream_id = "mod_tx_plan"
    key_properties = ["mod_tx_plan_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanClientProg(IncrementalStream):
    table_name = "mod_tx_plan_client_prog"
    tap_stream_id = "mod_tx_plan_client_prog"
    key_properties = ["mod_tx_plan_client_prog_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanEntity(IncrementalStream):
    table_name = "mod_tx_plan_entity"
    tap_stream_id = "mod_tx_plan_entity"
    key_properties = ["mod_tx_plan_entity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanEntityAct(IncrementalStream):
    table_name = "mod_tx_plan_entity_act"
    tap_stream_id = "mod_tx_plan_entity_act"
    key_properties = ["mod_tx_plan_entity_act_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanEntityHx(IncrementalStream):
    table_name = "mod_tx_plan_entity_hx"
    tap_stream_id = "mod_tx_plan_entity_hx"
    key_properties = ["mod_tx_plan_entity_hx_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanEntityInfo(IncrementalStream):

    table_name = "mod_tx_plan_entity_info"
    tap_stream_id = "mod_tx_plan_entity_info"
    key_properties = ["mod_tx_plan_entity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanInfo(IncrementalStream):

    table_name = "mod_tx_plan_info"
    tap_stream_id = "mod_tx_plan_info"
    key_properties = ["mod_tx_plan_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanNote(IncrementalStream):

    table_name = "mod_tx_plan_note"
    tap_stream_id = "mod_tx_plan_note"
    key_properties = ["mod_tx_plan_note_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModTxPlanNoteAddr(IncrementalStream):

    table_name = "mod_tx_plan_note_addr"
    tap_stream_id = "mod_tx_plan_note_addr"
    key_properties = ["mod_tx_plan_note_addr_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ModVitals(IncrementalStream):

    table_name = "mod_vitals"
    tap_stream_id = "mod_vitals"
    key_properties = ["mod_vitals_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Module(IncrementalStream):

    table_name = "module"
    tap_stream_id = "module"
    key_properties = ["module_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvBillingError(IncrementalStream):
    table_name = "mv_billing_error"
    tap_stream_id = "mv_billing_error"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvClaim(IncrementalStream):

    table_name = "mv_claim"
    tap_stream_id = "mv_claim"
    key_properties = ["claim_item_line_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvClient(IncrementalStream):
    table_name = "mv_client"
    tap_stream_id = "mv_client"
    key_properties = ["client_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvClientDiagnosis(IncrementalStream):
    table_name = "mv_client_diagnosis"
    tap_stream_id = "mv_client_diagnosis"
    key_properties = ["mod_tx_diag_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvClientDocument(IncrementalStream):

    table_name = "mv_client_document"
    tap_stream_id = "mv_client_document"
    key_properties = ["document_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvClientDsm5Diag(IncrementalStream):

    table_name = "mv_client_dsm5_diag"
    tap_stream_id = "mv_client_dsm5_diag"
    key_properties = ["mod_tx_dx_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvClientDsm5DiagDtl(IncrementalStream):

    table_name = "mv_client_dsm5_diag_dtl"
    tap_stream_id = "mv_client_dsm5_diag_dtl"
    key_properties = ["mod_tx_dx_diag_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvImpactData(IncrementalStream):

    table_name = "mv_impact_data"
    tap_stream_id = "mv_impact_data"
    key_properties = [None]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvImpactDataResponse(IncrementalStream):

    table_name = "mv_impact_data_response"
    tap_stream_id = "mv_impact_data_response"
    key_properties = ["mod_measure_response_dtl_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvPayment(IncrementalStream):
    table_name = "mv_payment"
    tap_stream_id = "mv_payment"
    key_properties = ["payment_post_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvScheduledActivities(IncrementalStream):
    table_name = "mv_scheduled_activities"
    tap_stream_id = "mv_scheduled_activities"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvStaff(IncrementalStream):
    table_name = "mv_staff"
    tap_stream_id = "mv_staff"
    key_properties = ["staff_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class MvTransactions(IncrementalStream):
    table_name = "mv_transactions"
    tap_stream_id = "mv_transactions"
    key_properties = ["transaction_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class NonBillableFailedAct(IncrementalStream):
    table_name = "non_billable_failed_act"
    tap_stream_id = "non_billable_failed_act"
    key_properties = ["non_billable_failed_act_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class NonBillableFailedClaim(IncrementalStream):
    table_name = "non_billable_failed_claim"
    tap_stream_id = "non_billable_failed_claim"
    key_properties = ["non_billable_failed_claim_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrdCode(IncrementalStream):
    table_name = "ord_code"
    tap_stream_id = "ord_code"
    key_properties = ["ord_code_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrdGeneric(IncrementalStream):
    table_name = "ord_generic"
    tap_stream_id = "ord_generic"
    key_properties = ["ord_generic_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrdLab(IncrementalStream):
    table_name = "ord_lab"
    tap_stream_id = "ord_lab"
    key_properties = ["ord_lab_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrdLabClinician(IncrementalStream):
    table_name = "ord_lab_clinician"
    tap_stream_id = "ord_lab_clinician"
    key_properties = ["ord_lab_clinician_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrdLabClinicianTest(IncrementalStream):
    table_name = "ord_lab_clinician_test"
    tap_stream_id = "ord_lab_clinician_test"
    key_properties = ["ord_lab_clinician_test_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrdMedication(IncrementalStream):
    table_name = "ord_medication"
    tap_stream_id = "ord_medication"
    key_properties = ["ord_medication_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrderConfigSetup(IncrementalStream):
    table_name = "order_config_setup"
    tap_stream_id = "order_config_setup"
    key_properties = ["order_config_setup_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrderConfigType(IncrementalStream):
    table_name = "order_config_type"
    tap_stream_id = "order_config_type"
    key_properties = ["order_config_type_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrderGroup(IncrementalStream):
    table_name = "order_group"
    tap_stream_id = "order_group"
    key_properties = ["order_group_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrderMaster(IncrementalStream):
    table_name = "order_master"
    tap_stream_id = "order_master"
    key_properties = ["order_master_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrderMasterType(IncrementalStream):
    table_name = "order_master_type"
    tap_stream_id = "order_master_type"
    key_properties = ["order_master_type_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrderModule(IncrementalStream):
    table_name = "order_module"
    tap_stream_id = "order_module"
    key_properties = ["order_module_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrderModuleStatus(IncrementalStream):
    table_name = "order_module_status"
    tap_stream_id = "order_module_status"
    key_properties = ["order_module_status_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Organization(IncrementalStream):
    table_name = "organization"
    tap_stream_id = "organization"
    key_properties = ["organization_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrganizationConfig(IncrementalStream):
    table_name = "organization_config"
    tap_stream_id = "organization_config"
    key_properties = ["organization_config_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class OrganizationRelative(IncrementalStream):
    table_name = "organization_relative"
    tap_stream_id = "organization_relative"
    key_properties = ["organization_relative_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Payer(IncrementalStream):
    table_name = "payer"
    tap_stream_id = "payer"
    key_properties = ["payer_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerOrg(IncrementalStream):
    table_name = "payer_org"
    tap_stream_id = "payer_org"
    key_properties = ["payer_org_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPanel(IncrementalStream):
    table_name = "payer_panel"
    tap_stream_id = "payer_panel"
    key_properties = ["payer_panel_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPanelOrgMap(IncrementalStream):
    table_name = "payer_panel_org_map"
    tap_stream_id = "payer_panel_org_map"
    key_properties = ["payer_panel_org_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPlan(IncrementalStream):
    table_name = "payer_plan"
    tap_stream_id = "payer_plan"
    key_properties = ["payer_plan_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPlanBenefit(IncrementalStream):
    table_name = "payer_plan_benefit"
    tap_stream_id = "payer_plan_benefit"
    key_properties = ["payer_plan_benefit_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPlanBenefitFee(IncrementalStream):
    table_name = "payer_plan_benefit_fee"
    tap_stream_id = "payer_plan_benefit_fee"
    key_properties = ["payer_plan_benefit_fee_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPlanConfig(IncrementalStream):
    table_name = "payer_plan_config"
    tap_stream_id = "payer_plan_config"
    key_properties = ["payer_plan_config_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPlanContact(IncrementalStream):
    table_name = "payer_plan_contact"
    tap_stream_id = "payer_plan_contact"
    key_properties = ["payer_plan_contact_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerPlanOrg(IncrementalStream):
    table_name = "payer_plan_org"
    tap_stream_id = "payer_plan_org"
    key_properties = ["payer_plan_org_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PayerProvider(IncrementalStream):
    table_name = "payer_provider"
    tap_stream_id = "payer_provider"
    key_properties = ["payer_provider_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PaymentActivity(IncrementalStream):
    table_name = "payment_activity"
    tap_stream_id = "payment_activity"
    key_properties = ["payment_activity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PaymentClaimAdjustment(IncrementalStream):
    table_name = "payment_claim_adjustment"
    tap_stream_id = "payment_claim_adjustment"
    key_properties = ["payment_claim_adjustment_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PaymentDetail(IncrementalStream):

    table_name = "payment_detail"
    tap_stream_id = "payment_detail"
    key_properties = ["payment_detail_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PaymentLine(IncrementalStream):
    table_name = "payment_line"
    tap_stream_id = "payment_line"
    key_properties = ["payment_line_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PaymentPost(IncrementalStream):
    table_name = "payment_post"
    tap_stream_id = "payment_post"
    key_properties = ["payment_post_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Person(IncrementalStream):
    table_name = "person"
    tap_stream_id = "person"
    key_properties = ["person_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonAddress(IncrementalStream):
    table_name = "person_address"
    tap_stream_id = "person_address"
    key_properties = ["person_address_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonAlias(IncrementalStream):
    table_name = "person_alias"
    tap_stream_id = "person_alias"
    key_properties = ["person_alias_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonContact(IncrementalStream):
    table_name = "person_contact"
    tap_stream_id = "person_contact"
    key_properties = ["person_contact_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonContactPhone(IncrementalStream):
    table_name = "person_contact_phone"
    tap_stream_id = "person_contact_phone"
    key_properties = ["person_contact_phone_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonDemo(IncrementalStream):
    table_name = "person_demo"
    tap_stream_id = "person_demo"
    key_properties = ["person_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonDemoDscData(IncrementalStream):
    table_name = "person_demo_dsc_data"
    tap_stream_id = "person_demo_dsc_data"
    key_properties = ["person_demo_dsc_data_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonName(IncrementalStream):
    table_name = "person_name"
    tap_stream_id = "person_name"
    key_properties = ["person_name_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PersonReminderPref(IncrementalStream):
    table_name = "person_reminder_pref"
    tap_stream_id = "person_reminder_pref"
    key_properties = ["person_reminder_pref_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class PrivilegeGroup(IncrementalStream):
    table_name = "privilege_group"
    tap_stream_id = "privilege_group"
    key_properties = ["privilege_group_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Procedure(IncrementalStream):
    table_name = "procedure"
    tap_stream_id = "procedure"
    key_properties = ["procedure_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ProcedureFee(IncrementalStream):
    table_name = "procedure_fee"
    tap_stream_id = "procedure_fee"
    key_properties = ["procedure_fee_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Program(IncrementalStream):
    table_name = "program"
    tap_stream_id = "program"
    key_properties = ["program_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ProgramOrgMap(IncrementalStream):
    table_name = "program_org_map"
    tap_stream_id = "program_org_map"
    key_properties = ["program_org_map_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class QsiUser(IncrementalStream):
    table_name = "qsi_user"
    tap_stream_id = "qsi_user"
    key_properties = ["qsi_user_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class QsiUserDate(IncrementalStream):
    table_name = "qsi_user_date"
    tap_stream_id = "qsi_user_date"
    key_properties = ["qsi_user_date_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ReferralSource(IncrementalStream):
    table_name = "referral_source"
    tap_stream_id = "referral_source"
    key_properties = ["referral_source_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Refund(IncrementalStream):
    table_name = "refund"
    tap_stream_id = "refund"
    key_properties = ["refund_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class RefundActivity(IncrementalStream):
    table_name = "refund_activity"
    tap_stream_id = "refund_activity"
    key_properties = ["refund_activity_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ScannedDocument(IncrementalStream):
    table_name = "scanned_document"
    tap_stream_id = "scanned_document"
    key_properties = ["scanned_document_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ScannedDocumentKeyword(IncrementalStream):
    table_name = "scanned_document_keyword"
    tap_stream_id = "scanned_document_keyword"
    key_properties = ["scanned_document_keyword_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ServiceDoc(IncrementalStream):
    table_name = "service_doc"
    tap_stream_id = "service_doc"
    key_properties = ["service_doc_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ServiceDocMatrix(IncrementalStream):
    table_name = "service_doc_matrix"
    tap_stream_id = "service_doc_matrix"
    key_properties = ["service_doc_matrix_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ServiceDocModule(IncrementalStream):
    table_name = "service_doc_module"
    tap_stream_id = "service_doc_module"
    key_properties = ["service_doc_module_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ServiceDocReject(IncrementalStream):
    table_name = "service_doc_reject"
    tap_stream_id = "service_doc_reject"
    key_properties = ["service_doc_reject_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ServiceDocSetup(IncrementalStream):
    table_name = "service_doc_setup"
    tap_stream_id = "service_doc_setup"
    key_properties = ["service_doc_setup_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class ServiceLocationCode(IncrementalStream):
    table_name = "service_location_code"
    tap_stream_id = "service_location_code"
    key_properties = ["service_location_code_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class SrpEpisode(IncrementalStream):
    table_name = "srp_episode"
    tap_stream_id = "srp_episode"
    key_properties = ["srp_episode_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Staff(IncrementalStream):
    table_name = "staff"
    tap_stream_id = "staff"
    key_properties = ["staff_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffCredential(IncrementalStream):
    table_name = "staff_credential"
    tap_stream_id = "staff_credential"
    key_properties = ["staff_credential_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffCredentialPrimary(IncrementalStream):
    table_name = "staff_credential_primary"
    tap_stream_id = "staff_credential_primary"
    key_properties = ["staff_credential_primary_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffHistory(IncrementalStream):
    table_name = "staff_history"
    tap_stream_id = "staff_history"
    key_properties = ["staff_history_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffHistoryData(IncrementalStream):
    table_name = "staff_history_data"
    tap_stream_id = "staff_history_data"
    key_properties = ["staff_history_data_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffHistoryOrg(IncrementalStream):
    table_name = "staff_history_org"
    tap_stream_id = "staff_history_org"
    key_properties = ["staff_history_org_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffPrivilege(IncrementalStream):
    table_name = "staff_privilege"
    tap_stream_id = "staff_privilege"
    key_properties = ["staff_privilege_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffShift(IncrementalStream):
    table_name = "staff_shift"
    tap_stream_id = "staff_shift"
    key_properties = ["staff_shift_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StaffSupervisoryGroup(IncrementalStream):
    table_name = "staff_supervisory_group"
    tap_stream_id = "staff_supervisory_group"
    key_properties = ["staff_supervisory_group_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StateReportingBatch(IncrementalStream):
    table_name = "state_reporting_batch"
    tap_stream_id = "state_reporting_batch"
    key_properties = ["state_reporting_batch_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class StateReportingBatchDtl(IncrementalStream):
    table_name = "state_reporting_batch_dtl"
    tap_stream_id = "state_reporting_batch_dtl"
    key_properties = ["state_reporting_batch_dtl_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TranType(IncrementalStream):
    table_name = "tran_type"
    tap_stream_id = "tran_type"
    key_properties = ["tran_type_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TransReason(IncrementalStream):
    table_name = "trans_reason"
    tap_stream_id = "trans_reason"
    key_properties = ["trans_reason_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class Transaction(IncrementalStream):
    table_name = "transaction"
    tap_stream_id = "transaction"
    key_properties = ["transaction_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TransactionPeriod(IncrementalStream):
    table_name = "transaction_period"
    tap_stream_id = "transaction_period"
    key_properties = ["transaction_period_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TreatmentPlanGrid(IncrementalStream):
    table_name = "treatment_plan_grid"
    tap_stream_id = "treatment_plan_grid"
    key_properties = ["treatment_plan_grid_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TreatmentPlanGridAssmt(IncrementalStream):
    table_name = "treatment_plan_grid_assmt"
    tap_stream_id = "treatment_plan_grid_assmt"
    key_properties = ["treatment_plan_grid_assmt_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TreatmentPlanGridDiag(IncrementalStream):
    table_name = "treatment_plan_grid_diag"
    tap_stream_id = "treatment_plan_grid_diag"
    key_properties = ["treatment_plan_grid_diag_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TreatmentPlanGridGoal(IncrementalStream):
    table_name = "treatment_plan_grid_goal"
    tap_stream_id = "treatment_plan_grid_goal"
    key_properties = ["treatment_plan_grid_goal_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TreatmentPlanGridLab(IncrementalStream):
    table_name = "treatment_plan_grid_lab"
    tap_stream_id = "treatment_plan_grid_lab"
    key_properties = ["treatment_plan_grid_lab_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TreatmentPlanGridObj(IncrementalStream):
    table_name = "treatment_plan_grid_obj"
    tap_stream_id = "treatment_plan_grid_obj"
    key_properties = ["treatment_plan_grid_obj_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TxPlanGridObjInt(IncrementalStream):
    table_name = "tx_plan_grid_obj_int"
    tap_stream_id = "tx_plan_grid_obj_int"
    key_properties = ["tx_plan_grid_obj_int_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


class TxPlanGridSubProb(IncrementalStream):
    table_name = "tx_plan_grid_sub_prob"
    tap_stream_id = "tx_plan_grid_sub_prob"
    key_properties = ["tx_plan_grid_sub_prob_id"]
    replication_method = "INCREMENTAL"
    valid_replication_keys = ["last_commit_time"]
    replication_key = "last_commit_time"


STREAMS_0 = {
    "activity": Activity,
    "activity_detail": ActivityDetail,
    "activity_error": ActivityError,
    "activity_log": ActivityLog,
    "activity_procedure_addon": ActivityProcedureAddon,
    "activity_procedure_clm": ActivityProcedureClm,
    "activity_procedure_clm_mod": ActivityProcedureClmMod,
    "activity_procedure_matrix": ActivityProcedureMatrix,
    "activity_program_matrix": ActivityProgramMatrix,
    "addendum": Addendum,
    "address": Address,
    "admin_co_pay_matrix": AdminCoPayMatrix,
    "admin_co_pay_matrix_lic": AdminCoPayMatrixLic,
    "admin_group": AdminGroup,
    "admin_order_status": AdminOrderStatus,
    "alert": Alert,
    "allergy_entry": AllergyEntry,
    "audit_dataedit": AuditDataedit,
    "audit_delete_values": AuditDeleteValues,
    # "audit_log": AuditLog,
    "audit_page_title": AuditPageTitle,
    "audit_row_delete": AuditRowDelete,
    "cash_sheet": CashSheet,
    "cash_sheet_line": CashSheetLine,
    "claim": Claim,
    "claim_batch": ClaimBatch,
    "claim_batch_line": ClaimBatchLine,
    "claim_bill_next": ClaimBillNext,
    "claim_diag": ClaimDiag,
    "claim_engine_run": ClaimEngineRun,
    "claim_error": ClaimError,
    "claim_item": ClaimItem,
    "claim_item_activity": ClaimItemActivity,
    "claim_item_edit_audit": ClaimItemEditAudit,
    "claim_item_line": ClaimItemLine,
    "claim_item_modifier": ClaimItemModifier,
    "claim_note": ClaimNote,
    "claim_rollup": ClaimRollup,
}

STREAMS_1 = {
    "client": Client,
    "claim_followup_comment": ClaimFollowupComment,
    "client_co_pay": ClientCoPay,
    "client_liability": ClientLiability,
    "client_view": ClientView,
    "clinical_recon": ClinicalRecon,
    "client_allergy": ClientAllergy,
    "client_auth_procedure": ClientAuthProcedure,
    "client_balance": ClientBalance,
    "client_black_box": ClientBlackBox,
    "client_black_box_staff": ClientBlackBoxStaff,
    "client_episode": ClientEpisode,
    "client_episode_org_map": ClientEpisodeOrgMap,
    "client_episode_prefs": ClientEpisodePrefs,
    "client_group": ClientGroup,
    "client_guarantor": ClientGuarantor,
    "client_medication": ClientMedication,
    "client_message": ClientMessage,
    "client_payer_auth": ClientPayerAuth,
    "client_payer_plan": ClientPayerPlan,
    "client_payer_plan_date": ClientPayerPlanDate,
    "client_program": ClientProgram,
    "client_program_date": ClientProgramDate,
    "client_scanned_document": ClientScannedDocument,
    "client_sliding_scale": ClientSlidingScale,
    "client_staff": ClientStaff,
    "client_view_attempt": ClientViewAttempt,
    "code_system": CodeSystem,
    "collection_assignment": CollectionAssignment,
    "cs_batch": CsBatch,
    "cs_batch_client": CsBatchClient,
    "cs_batch_client_aging": CsBatchClientAging,
    "cs_batch_client_claim": CsBatchClientClaim,
    "cs_batch_client_claim_tran": CsBatchClientClaimTran,
    "deposit": Deposit,
    "deposit_activity": DepositActivity,
    "deposit_audit": DepositAudit,
    "descriptor": Descriptor,
    "descriptor_mapped_value": DescriptorMappedValue,
    "document": Document,
    "document_audit": DocumentAudit,
    "document_grouping": DocumentGrouping,
    "document_signature": DocumentSignature,
    "document_signature_pad": DocumentSignaturePad,
}

STREAMS_2 = {
    "dsm_diag_category": DsmDiagCategory,
    "dsm_diag_category_range": DsmDiagCategoryRange,
    "dsm_diagnosis": DsmDiagnosis,
    "dyn_hcfa": DynHcfa,
    "edi_270_batch": Edi270Batch,
    "edi_270_detail": Edi270Detail,
    "edi_271": Edi271,
    "edi_271_eb_dates": Edi271EbDates,
    "edi_271_eligible": Edi271Eligible,
    "edi_271_reference": Edi271Reference,
    "edi_271_subscriber": Edi271Subscriber,
    "edi_271_subscriber_benefit": Edi271SubscriberBenefit,
    "edi_835_adj_org": Edi835AdjOrg,
    "edi_835_adj_org_matrix": Edi835AdjOrgMatrix,
    "edi_835_adj_org_payer_plan": Edi835AdjOrgPayerPlan,
    "failed_login": FailedLogin,
    "edi_835": Edi835,
    "edi_835_adjustment": Edi835Adjustment,
    "edi_835_adjustment_reason": Edi835AdjustmentReason,
    "edi_835_plb": Edi835Plb,
    "edi_835_reference": Edi835Reference,
    # "edi_835_service": Edi835Service,
    "edi_835_transaction": Edi835Transaction,
    "edi_837": Edi837,
    "edi_837_element": Edi837Element,
    "edi_837_level": Edi837Level,
    "edi_code": EdiCode,
    "edi_type": EdiType,
    "episode_type": EpisodeType,
    "error": Error,
    "erx_allergy": ErxAllergy,
    "erx_client": ErxClient,
    "erx_drug": ErxDrug,
    "erx_medication": ErxMedication,
    "erx_notification": ErxNotification,
    "erx_pharmacy": ErxPharmacy,
    "erx_prescription": ErxPrescription,
    "erx_prescription_status": ErxPrescriptionStatus,
    "erx_sig": ErxSig,
    "guarantor": Guarantor,
    "intake_tracking": IntakeTracking,
    "ip_log": IpLog,
    "licensure": Licensure,
    "macsis_adm_dis": MacsisAdmDis,
    "macsis_adm_dis_data": MacsisAdmDisData,
    "master_modifier": MasterModifier,
}

STREAMS_3 = {
    "cf_data": CfData,
    "cf_data_hist": CfDataHist,
    "master_modifier_detail": MasterModifierDetail,
    "master_modifier_org_map": MasterModifierOrgMap,
    "measure": Measure,
    "measure_question": MeasureQuestion,
    "measure_question_val": MeasureQuestionVal,
    "measure_section": MeasureSection,
    "measure_subtotal": MeasureSubtotal,
    "medication_entry": MedicationEntry,
    "menu": Menu,
    "menu_org_map": MenuOrgMap,
    "menu_priv": MenuPriv,
    "menu_system": MenuSystem,
    "menu_system_org_map": MenuSystemOrgMap,
    "mod_call_log": ModCallLog,
    "mod_eval_management": ModEvalManagement,
    "mod_lab_result": ModLabResult,
    "mod_lab_result_dtl": ModLabResultDtl,
    "mod_medication": ModMedication,
    "mod_memo_note": ModMemoNote,
    "mod_service_addition": ModServiceAddition,
    "mod_sub_abuse_dtl_dsc": ModSubAbuseDtlDsc,
    "mod_substance_abuse": ModSubstanceAbuse,
    "mod_substance_abuse_dsc": ModSubstanceAbuseDsc,
    "mod_substance_abuse_dtl": ModSubstanceAbuseDtl,
    "mod_teds_noms": ModTedsNoms,
    "mod_tplan_entity": ModTplanEntity,
    "mod_tplan_entity_dtl": ModTplanEntityDtl,
    "mod_tplan_entity_map": ModTplanEntityMap,
    "mod_tplan_master": ModTplanMaster,
    "mod_tx_dx": ModTxDx,
    "mod_tx_dx_code": ModTxDxCode,
}
STREAMS_4 = {
    "mod_manual_med_rec": ModManualMedRec,
    "mod_trans_discharge": ModTransDischarge,
    "mod_tx_diag": ModTxDiag,
    "mod_tx_diag_axis": ModTxDiagAxis,
    "mod_tx_dx_diag_spec_sev": ModTxDxDiagSpecSev,
    "mod_tx_dx_code_spec_sev": ModTxDxCodeSpecSev,
    "mod_tx_dx_diag": ModTxDxDiag,
    "mod_tx_dx_info": ModTxDxInfo,
    "mod_tx_plan": ModTxPlan,
    "mod_tx_plan_client_prog": ModTxPlanClientProg,
    "mod_tx_plan_info": ModTxPlanInfo,
    "mod_tx_plan_note": ModTxPlanNote,
    "mod_tx_plan_note_addr": ModTxPlanNoteAddr,
    "mod_vitals": ModVitals,
    "module": Module,
    "mv_billing_error": MvBillingError,
    "mv_claim": MvClaim,
    "mv_client": MvClient,
    "mv_client_diagnosis": MvClientDiagnosis,
    "mv_client_document": MvClientDocument,
    "mv_client_dsm5_diag": MvClientDsm5Diag,
    "mv_client_dsm5_diag_dtl": MvClientDsm5DiagDtl,
    "mv_payment": MvPayment,
    "mv_scheduled_activities": MvScheduledActivities,
    "mv_staff": MvStaff,
    "mv_transactions": MvTransactions,
    "non_billable_failed_act": NonBillableFailedAct,
    "non_billable_failed_claim": NonBillableFailedClaim,
    "ord_code": OrdCode,
    "ord_lab": OrdLab,
    "ord_medication": OrdMedication,
    "order_config_setup": OrderConfigSetup,
    "order_config_type": OrderConfigType,
    "order_group": OrderGroup,
}

STREAMS_5 = {
    # "mv_impact_data": MvImpactData,
    "mv_impact_data_response": MvImpactDataResponse,
    "order_module": OrderModule,
    "order_master": OrderMaster,
    "order_master_type": OrderMasterType,
    "order_module_status": OrderModuleStatus,
    "organization": Organization,
    "organization_config": OrganizationConfig,
    "payer": Payer,
    "payer_panel": PayerPanel,
    "payer_panel_org_map": PayerPanelOrgMap,
    "payer_plan": PayerPlan,
    "payer_plan_benefit": PayerPlanBenefit,
    "payer_plan_benefit_fee": PayerPlanBenefitFee,
    "payer_plan_config": PayerPlanConfig,
    "payer_plan_contact": PayerPlanContact,
    "payer_plan_org": PayerPlanOrg,
    "payer_provider": PayerProvider,
    "payment_activity": PaymentActivity,
    "payment_claim_adjustment": PaymentClaimAdjustment,
    "payment_post": PaymentPost,
    "person": Person,
    "person_address": PersonAddress,
    "person_alias": PersonAlias,
    "person_contact": PersonContact,
    "person_contact_phone": PersonContactPhone,
    "person_demo": PersonDemo,
    "person_demo_dsc_data": PersonDemoDscData,
    "person_name": PersonName,
    "person_reminder_pref": PersonReminderPref,
    "privilege_group": PrivilegeGroup,
    "procedure_fee": ProcedureFee,
    "program": Program,
    "program_org_map": ProgramOrgMap,
}

STREAMS_6 = {
    "qsi_user": QsiUser,
    "qsi_user_date": QsiUserDate,
    "referral_source": ReferralSource,
    "refund": Refund,
    "refund_activity": RefundActivity,
    "scanned_document": ScannedDocument,
    "scanned_document_keyword": ScannedDocumentKeyword,
    "service_doc": ServiceDoc,
    "service_doc_matrix": ServiceDocMatrix,
    "service_doc_module": ServiceDocModule,
    "service_doc_reject": ServiceDocReject,
    "service_doc_setup": ServiceDocSetup,
    "service_location_code": ServiceLocationCode,
    "staff": Staff,
    "staff_credential": StaffCredential,
    "staff_credential_primary": StaffCredentialPrimary,
    "staff_history": StaffHistory,
    "staff_history_org": StaffHistoryOrg,
    "staff_privilege": StaffPrivilege,
    "staff_shift": StaffShift,
    "staff_supervisory_group": StaffSupervisoryGroup,
    "state_reporting_batch": StateReportingBatch,
    "state_reporting_batch_dtl": StateReportingBatchDtl,
    "tran_type": TranType,
    "trans_reason": TransReason,
    "transaction": Transaction,
    "treatment_plan_grid": TreatmentPlanGrid,
    "treatment_plan_grid_diag": TreatmentPlanGridDiag,
    "treatment_plan_grid_goal": TreatmentPlanGridGoal,
    "treatment_plan_grid_obj": TreatmentPlanGridObj,
    "tx_plan_grid_obj_int": TxPlanGridObjInt,
    "tx_plan_grid_sub_prob": TxPlanGridSubProb,
}

STREAMS = [STREAMS_0, STREAMS_1, STREAMS_2, STREAMS_3, STREAMS_4, STREAMS_5, STREAMS_6]

# STREAMS = {
#     "activity": Activity,
#     "activity_detail": ActivityDetail,
#     "activity_error": ActivityError,
#     "activity_log": ActivityLog,
#     "activity_procedure_addon": ActivityProcedureAddon,
#     "activity_procedure_clm": ActivityProcedureClm,
#     "activity_procedure_clm_mod": ActivityProcedureClmMod,
#     "activity_procedure_matrix": ActivityProcedureMatrix,
#     "activity_program_matrix": ActivityProgramMatrix,
#     "addendum": Addendum,
#     "address": Address,
#     "admin_co_pay_matrix": AdminCoPayMatrix,
#     "admin_co_pay_matrix_lic": AdminCoPayMatrixLic,
#     "audit_dataedit": AuditDataedit,
#     "audit_delete_values": AuditDeleteValues,
#     "audit_log": AuditLog,
#     "audit_page_title": AuditPageTitle,
#     "audit_row_delete": AuditRowDelete,
#     "admin_group": AdminGroup,
#     "admin_order_status": AdminOrderStatus,
#     "alert": Alert,
#     "allergy_entry": AllergyEntry,
#     "cash_sheet": CashSheet,
#     "cash_sheet_line": CashSheetLine,
#     "claim": Claim,
#     "claim_batch": ClaimBatch,
#     "claim_batch_line": ClaimBatchLine,
#     "claim_bill_next": ClaimBillNext,
#     "claim_diag": ClaimDiag,
#     "claim_engine_run": ClaimEngineRun,
#     "claim_error": ClaimError,
#     "claim_item": ClaimItem,
#     "claim_item_activity": ClaimItemActivity,
#     "claim_item_edit_audit": ClaimItemEditAudit,
#     "claim_item_line": ClaimItemLine,
#     "claim_item_modifier": ClaimItemModifier,
#     "claim_note": ClaimNote,
#     "claim_rollup": ClaimRollup,
#     "client": Client,
#     "claim_followup_comment": ClaimFollowupComment,
#     "client_co_pay": ClientCoPay,
#     "client_liability": ClientLiability,
#     "client_view": ClientView,
#     "clinical_recon": ClinicalRecon,
#     "client_allergy": ClientAllergy,
#     "client_auth_procedure": ClientAuthProcedure,
#     "client_balance": ClientBalance,
#     "client_black_box": ClientBlackBox,
#     "client_black_box_staff": ClientBlackBoxStaff,
#     "client_episode": ClientEpisode,
#     "client_episode_org_map": ClientEpisodeOrgMap,
#     "client_episode_prefs": ClientEpisodePrefs,
#     "client_group": ClientGroup,
#     "client_guarantor": ClientGuarantor,
#     "client_medication": ClientMedication,
#     "client_message": ClientMessage,
#     "client_payer_auth": ClientPayerAuth,
#     "client_payer_plan": ClientPayerPlan,
#     "client_payer_plan_date": ClientPayerPlanDate,
#     "client_program": ClientProgram,
#     "client_program_date": ClientProgramDate,
#     "client_scanned_document": ClientScannedDocument,
#     "client_sliding_scale": ClientSlidingScale,
#     "client_staff": ClientStaff,
#     "client_view_attempt": ClientViewAttempt,
#     "code_system": CodeSystem,
#     "collection_assignment": CollectionAssignment,
#     "cs_batch": CsBatch,
#     "cs_batch_client": CsBatchClient,
#     "cs_batch_client_aging": CsBatchClientAging,
#     "cs_batch_client_claim": CsBatchClientClaim,
#     "cs_batch_client_claim_tran": CsBatchClientClaimTran,
#     "deposit": Deposit,
#     "deposit_activity": DepositActivity,
#     "deposit_audit": DepositAudit,
#     "descriptor": Descriptor,
#     "descriptor_mapped_value": DescriptorMappedValue,
#     "document": Document,
#     "document_audit": DocumentAudit,
#     "document_grouping": DocumentGrouping,
#     "document_signature": DocumentSignature,
#     "document_signature_pad": DocumentSignaturePad,
#     "dsm_diag_category": DsmDiagCategory,
#     "dsm_diag_category_range": DsmDiagCategoryRange,
#     "dsm_diagnosis": DsmDiagnosis,
#     "dyn_hcfa": DynHcfa,
#     "edi_270_batch": Edi270Batch,
#     "edi_270_detail": Edi270Detail,
#     "edi_271": Edi271,
#     "edi_271_eb_dates": Edi271EbDates,
#     "edi_271_eligible": Edi271Eligible,
#     "edi_271_reference": Edi271Reference,
#     "edi_835": Edi835,
#     "edi_835_adjustment": Edi835Adjustment,
#     "edi_835_adjustment_reason": Edi835AdjustmentReason,
#     "edi_835_plb": Edi835Plb,
#     "edi_835_reference": Edi835Reference,
#     "edi_835_service": Edi835Service,
#     "edi_835_transaction": Edi835Transaction,
#     "edi_837": Edi837,
#     "edi_837_element": Edi837Element,
#     "edi_837_level": Edi837Level,
#     "edi_code": EdiCode,
#     "edi_type": EdiType,
#     "episode_type": EpisodeType,
#     "error": Error,
#     "erx_allergy": ErxAllergy,
#     "erx_client": ErxClient,
#     "erx_drug": ErxDrug,
#     "erx_medication": ErxMedication,
#     "erx_notification": ErxNotification,
#     "erx_pharmacy": ErxPharmacy,
#     "erx_prescription": ErxPrescription,
#     "erx_prescription_status": ErxPrescriptionStatus,
#     "erx_sig": ErxSig,
#     "edi_271_subscriber": Edi271Subscriber,
#     "edi_271_subscriber_benefit": Edi271SubscriberBenefit,
#     "edi_835_adj_org": Edi835AdjOrg,
#     "edi_835_adj_org_matrix": Edi835AdjOrgMatrix,
#     "edi_835_adj_org_payer_plan": Edi835AdjOrgPayerPlan,
#     "failed_login": FailedLogin,
#     "guarantor": Guarantor,
#     "intake_tracking": IntakeTracking,
#     "ip_log": IpLog,
#     "licensure": Licensure,
#     "macsis_adm_dis": MacsisAdmDis,
#     "macsis_adm_dis_data": MacsisAdmDisData,
#     "master_modifier": MasterModifier,
#     "master_modifier_detail": MasterModifierDetail,
#     "master_modifier_org_map": MasterModifierOrgMap,
#     "measure": Measure,
#     "measure_question": MeasureQuestion,
#     "measure_question_val": MeasureQuestionVal,
#     "measure_section": MeasureSection,
#     "measure_subtotal": MeasureSubtotal,
#     "medication_entry": MedicationEntry,
#     "menu": Menu,
#     "menu_org_map": MenuOrgMap,
#     "menu_priv": MenuPriv,
#     "menu_system": MenuSystem,
#     "menu_system_org_map": MenuSystemOrgMap,
#     "mod_call_log": ModCallLog,
#     "mod_eval_management": ModEvalManagement,
#     "mod_lab_result": ModLabResult,
#     "mod_lab_result_dtl": ModLabResultDtl,
#     "mod_medication": ModMedication,
#     "mod_memo_note": ModMemoNote,
#     "mod_service_addition": ModServiceAddition,
#     "mod_sub_abuse_dtl_dsc": ModSubAbuseDtlDsc,
#     "mod_substance_abuse": ModSubstanceAbuse,
#     "mod_substance_abuse_dsc": ModSubstanceAbuseDsc,
#     "mod_substance_abuse_dtl": ModSubstanceAbuseDtl,
#     "mod_teds_noms": ModTedsNoms,
#     "mod_tplan_entity": ModTplanEntity,
#     "mod_tplan_entity_dtl": ModTplanEntityDtl,
#     "mod_tplan_entity_map": ModTplanEntityMap,
#     "mod_tplan_master": ModTplanMaster,
#     "mod_tx_dx": ModTxDx,
#     "mod_tx_dx_code": ModTxDxCode,
#     "mod_tx_dx_code_spec_sev": ModTxDxCodeSpecSev,
#     "mod_tx_dx_diag": ModTxDxDiag,
#     "mod_tx_dx_info": ModTxDxInfo,
#     "mod_tx_plan": ModTxPlan,
#     "mod_tx_plan_client_prog": ModTxPlanClientProg,
#     "mod_tx_plan_info": ModTxPlanInfo,
#     "mod_tx_plan_note": ModTxPlanNote,
#     "mod_tx_plan_note_addr": ModTxPlanNoteAddr,
#     "mod_vitals": ModVitals,
#     "mod_manual_med_rec": ModManualMedRec,
#     "mod_trans_discharge": ModTransDischarge,
#     "mod_tx_diag": ModTxDiag,
#     "mod_tx_diag_axis": ModTxDiagAxis,
#     "mod_tx_dx_diag_spec_sev": ModTxDxDiagSpecSev,
#     "module": Module,
#     "mv_billing_error": MvBillingError,
#     "mv_claim": MvClaim,
#     "mv_client": MvClient,
#     "mv_client_diagnosis": MvClientDiagnosis,
#     "mv_client_document": MvClientDocument,
#     "mv_client_dsm5_diag": MvClientDsm5Diag,
#     "mv_client_dsm5_diag_dtl": MvClientDsm5DiagDtl,
#     "mv_impact_data": MvImpactData,
#     "mv_impact_data_response": MvImpactDataResponse,
#     "order_module": OrderModule,
#     "treatment_plan_grid_diag": TreatmentPlanGridDiag,
#     "mv_payment": MvPayment,
#     "mv_scheduled_activities": MvScheduledActivities,
#     "mv_staff": MvStaff,
#     "mv_transactions": MvTransactions,
#     "non_billable_failed_act": NonBillableFailedAct,
#     "non_billable_failed_claim": NonBillableFailedClaim,
#     "ord_code": OrdCode,
#     "ord_lab": OrdLab,
#     "ord_medication": OrdMedication,
#     "order_config_setup": OrderConfigSetup,
#     "order_config_type": OrderConfigType,
#     "order_group": OrderGroup,
#     "order_master": OrderMaster,
#     "order_master_type": OrderMasterType,
#     "order_module_status": OrderModuleStatus,
#     "organization": Organization,
#     "organization_config": OrganizationConfig,
#     "payer": Payer,
#     "payer_panel": PayerPanel,
#     "payer_panel_org_map": PayerPanelOrgMap,
#     "payer_plan": PayerPlan,
#     "payer_plan_benefit": PayerPlanBenefit,
#     "payer_plan_benefit_fee": PayerPlanBenefitFee,
#     "payer_plan_config": PayerPlanConfig,
#     "payer_plan_contact": PayerPlanContact,
#     "payer_plan_org": PayerPlanOrg,
#     "payer_provider": PayerProvider,
#     "payment_activity": PaymentActivity,
#     "payment_claim_adjustment": PaymentClaimAdjustment,
#     "payment_post": PaymentPost,
#     "person": Person,
#     "person_address": PersonAddress,
#     "person_alias": PersonAlias,
#     "person_contact": PersonContact,
#     "person_contact_phone": PersonContactPhone,
#     "person_demo": PersonDemo,
#     "person_demo_dsc_data": PersonDemoDscData,
#     "person_name": PersonName,
#     "person_reminder_pref": PersonReminderPref,
#     "privilege_group": PrivilegeGroup,
#     "procedure_fee": ProcedureFee,
#     "program": Program,
#     "program_org_map": ProgramOrgMap,
#     "qsi_user": QsiUser,
#     "qsi_user_date": QsiUserDate,
#     "referral_source": ReferralSource,
#     "refund": Refund,
#     "refund_activity": RefundActivity,
#     "scanned_document": ScannedDocument,
#     "scanned_document_keyword": ScannedDocumentKeyword,
#     "service_doc": ServiceDoc,
#     "service_doc_matrix": ServiceDocMatrix,
#     "service_doc_module": ServiceDocModule,
#     "service_doc_reject": ServiceDocReject,
#     "service_doc_setup": ServiceDocSetup,
#     "service_location_code": ServiceLocationCode,
#     "staff": Staff,
#     "staff_credential": StaffCredential,
#     "staff_credential_primary": StaffCredentialPrimary,
#     "staff_history": StaffHistory,
#     "staff_history_org": StaffHistoryOrg,
#     "staff_privilege": StaffPrivilege,
#     "staff_shift": StaffShift,
#     "staff_supervisory_group": StaffSupervisoryGroup,
#     "state_reporting_batch": StateReportingBatch,
#     "state_reporting_batch_dtl": StateReportingBatchDtl,
#     "tran_type": TranType,
#     "trans_reason": TransReason,
#     "transaction": Transaction,
#     "treatment_plan_grid": TreatmentPlanGrid,
#     "treatment_plan_grid_goal": TreatmentPlanGridGoal,
#     "treatment_plan_grid_obj": TreatmentPlanGridObj,
#     "tx_plan_grid_obj_int": TxPlanGridObjInt,
#     "tx_plan_grid_sub_prob": TxPlanGridSubProb,
# }

# STREAMS_NOT_SYNCED = {
    # "act_proc_matrix_dsc": ActProcMatrixDsc,
    # "activity_detail_dsc": ActivityDetailDsc,
    # "activity_dsc": ActivityDsc,
    # "admin_co_pay": AdminCoPay,
    # No last_commit_time "cf_data": CfData,
    # No last_commit_time "cf_data_hist": CfDataHist,
    # Zero Data    'claim_bill_next_item': ClaimBillNextItem,
    # "claim_value_code": ClaimValueCode,
    # "client_auth_proc_modif": ClientAuthProcModif,
    # "client_co_pay_matrix": ClientCoPayMatrix,
    # "client_co_pay_matrix_lic": ClientCoPayMatrixLic,
    # "client_consent": ClientConsent,
    # "client_episode_triag": ClientEpisodeTriag,
    # "client_guarantor_mix": ClientGuarantorMix,
    # "client_liability_mem": ClientLiabilityMem,
    # Zero Data   'client_liability_mem_exp': ClientLiabilityMemExp,
    # "client_pcp": ClientPcp,
    # "client_pharmacy": ClientPharmacy,
    # "client_program_code": ClientProgramCode,
    # "client_program_unbillable": ClientProgramUnbillable,
    # "client_provider": ClientProvider,
    # "client_record_inv": ClientRecordInv,
    # "client_record_inv_change": ClientRecordInvChange,
    # "client_relationship": ClientRelationship,
    # "clinician_allergy_entry": ClinicianAllergyEntry,
    # "clinician_ord_medication": ClinicianOrdMedication,
    # "clinician_user": ClinicianUser,
    # "collection_assignment_clms": CollectionAssignmentClms,
    # "document_status": DocumentStatus,
    # "edi_271_request_val": Edi271RequestVal,
    # "ffs_batch": FfsBatch,
    # "ffs_batch_line": FfsBatchLine,
    # "ffs_batch_line_err": FfsBatchLineErr,
    # "ffs_batch_line_hx": FfsBatchLineHx,
    # "gl_code_activity": GlCodeActivity,
    # "gl_code_date": GlCodeDate,
    # "gl_code_org_prog": GlCodeOrgProg,
    # "gl_code_organization": GlCodeOrganization,
    # "gl_code_payer": GlCodePayer,
    # "gl_code_population": GlCodePopulation,
    # "gl_code_prog_act": GlCodeProgAct,
    # "gl_code_program": GlCodeProgram,
    # "gl_detail": GlDetail,
    # "gl_error": GlError,
    # "gl_map": GlMap,
    # "intake_followup": IntakeFollowup,
    # "location": Location,
    # "macsis_client_sig_pad": MacsisClientSigPad,
    # "macsis_enrollment_form": MacsisEnrollmentForm,
    # "macsis_enrollment_form_d": MacsisEnrollmentFormD,
    # "macsis_enrollment_verify": MacsisEnrollmentVerify,
    # "master_person_index": MasterPersonIndex,
    # "medication": Medication,
    # "medication_dispense": MedicationDispense,
    # "medication_org_map": MedicationOrgMap,
    # "mod_employmt": ModEmploymt,
    # "mod_goals_addr_summary": ModGoalsAddrSummary,
    # "mod_legal": ModLegal,
    # "mod_living_ed": ModLivingEd,
    # "mod_med_diag_cat": ModMedDiagCat,
    # "mod_pcp_signature": ModPcpSignature,
    # "mod_pcp_signature_cbx": ModPcpSignatureCbx,
    # "mod_referral": ModReferral,
    # "mod_service_detail": ModServiceDetail,
    # "mod_service_detail_sb": ModServiceDetailSb,
    # "mod_substance_abuse_date": ModSubstanceAbuseDate,
    # "mod_tobacco": ModTobacco,
    # "mod_tx_plan_entity": ModTxPlanEntity,
    # "mod_tx_plan_entity_act": ModTxPlanEntityAct,
    # "mod_tx_plan_entity_hx": ModTxPlanEntityHx,
    # Zero Data   'mod_tx_plan_entity_info': ModTxPlanEntityInfo,
    # "ord_generic": OrdGeneric,
    # "ord_lab_clinician": OrdLabClinician,
    # "ord_lab_clinician_test": OrdLabClinicianTest,
    # No Unique Id   'organization_relative': OrganizationRelative,
    # "payer_org": PayerOrg,
    # Zero Data   'payment_detail': PaymentDetail,
    # "payment_line": PaymentLine,
    # Broken Table   'procedure': Procedure,
    # "srp_episode": SrpEpisode,
    # "staff_history_data": StaffHistoryData,
    # "transaction_period": TransactionPeriod,
    # "treatment_plan_grid_assmt": TreatmentPlanGridAssmt,
    # "treatment_plan_grid_lab": TreatmentPlanGridLab
# }