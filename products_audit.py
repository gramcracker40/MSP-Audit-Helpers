from env_var import liongard_controller, get_msp_additions
from product_audits.cove_audit import cove_audit
from product_audits.s1_audit import s1_audit
from product_audits.huntress_audit import huntress_audit
from product_audits.rmm_audit import rmm_audit

# grabbing data to supply the individual audits
systems = liongard_controller.get_systems()
cw_additions = get_msp_additions()

# performing audits over the products listed below. Each function produces
# a neatly organized CSV file going over the company/site name and discrepancies
cove_audit(systems, cw_additions)
s1_audit(systems, cw_additions)
rmm_audit(cw_additions)
huntress_audit()
