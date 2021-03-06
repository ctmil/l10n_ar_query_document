from odoo import fields,models, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)



class CompConsultarWizard(models.TransientModel):
    _name = 'wizard.comp.consultar'
    _name = 'wizard.comp.consultar'

    journal_id = fields.Many2one('account.journal',string='Diario')
    doc_type = fields.Many2one('l10n_latam.document.type',string='Tipo Documento')
    doc_nro = fields.Integer('Nro Documento')

    def btn_confirm(self):
        pos_number = self.journal_id.l10n_ar_afip_pos_number
        doc_type = self.doc_type.code
        afip_ws = self.journal_id.afip_ws
        ws = self.journal_id.company_id.get_connection(afip_ws).connect()
        ws.CompConsultar(doc_type,pos_number,self.doc_nro)
        attributes = [
                'FechaCbte', 'CbteNro', 'PuntoVenta',
                'Vencimiento', 'ImpTotal', 'Resultado', 'CbtDesde', 'CbtHasta',
                'ImpTotal', 'ImpNeto', 'ImptoLiq', 'ImpOpEx', 'ImpTrib',
                'EmisionTipo', 'CAE', 'CAEA', 'XmlResponse']
        msg = ''
        title = _('Invoice number %s\n' % self.doc_nro)

        # TODO ver como hacer para que tome los enter en los mensajes
        for pu_attrin in attributes:
            msg += "%s: %s\n" % (
                pu_attrin, getattr(ws, pu_attrin))

        msg += " - ".join([
            ws.Excepcion,
            ws.ErrMsg,
            ws.Obs])
        # TODO parsear este response. buscar este metodo que puede ayudar
        # b = ws.ObtenerTagXml("CAE")
        # import xml.etree.ElementTree as ET
        # T = ET.fromstring(ws.XmlResponse)

        _logger.info('%s\n%s' % (title, msg))
        raise UserError(title + msg)

