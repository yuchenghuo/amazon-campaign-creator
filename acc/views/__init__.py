"""Views, one for each amazon campaign creator page."""
from acc.views.auth import login, edit_account
from acc.views.auto_disaggregation import auto_disaggregation_campaign
from acc.views.index import index
from acc.views.root_expansion import root_expansion_campaign
from acc.views.single_keyword import single_keyword_campaign
from acc.views.single_product import single_product_campaign
