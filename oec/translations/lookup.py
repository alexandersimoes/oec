# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

def get_translations():

    return {

        # Viz text formatter
        "share": _('Percent'),
        "export_val": _('Export Value'),
        "net_export_val": _('Net Export Value'),
        "import_val": _('Import Value'),
        "net_import_val": _('Net Import Value'),
        "market_val": _('Market Value'),
        "export_rca": _('Export RCA'),
        "import_rca": _('Import RCA'),
        "gdp": _('GDP'),
        "gdp_pc_constant": _('GDPpc (constant \'05 US$)'),
        "gdp_pc_current": _('GDPpc (current US$)'),
        "gdp_pc_constant_ppp": _('GDPpc PPP (constant \'11)'),
        "gdp_pc_current_ppp": _('GDPpc PPP (current)'),
        "eci": _('ECI'),
        "eci_rank": _('ECI Rank'),
        "id": _('ID'),
        "export_val_growth_pct": _('Annual Growth Rate (1 year)'),
        "export_val_growth_pct_5": _('Annual Growth Rate (5 year)'),
        "export_val_growth_val": _('Growth Value (1 year)'),
        "export_val_growth_val_5": _('Growth Value (5 year)'),
        "import_val_growth_pct": _('Annual Growth Rate (1 year)'),
        "import_val_growth_pct_5": _('Annual Growth Rate (5 year)'),
        "import_val_growth_val": _('Growth Value (1 year)'),
        "import_val_growth_val_5": _('Growth Value (5 year)'),

        # Javascript UI
        "loading": _("Loading..."),
        "loading_viz": _("Loading Visualization"),
        "no_results": _("We couldn't find any results.")

    }
