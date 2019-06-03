from odoo import models,fields


class Shipments(models.Model):
	_name = 'shipment.shipment'
	_description = 'Magento Invoices'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")
	packing_slip = fields.Char("Packing Slip")
	order = fields.Char("Order")
	order_date = fields.Date("Order Date")
	sold_to = fields.Many2one('shipment.shipment', string = "Sold To")
	ship_to = fields.Many2one('shipment.shipment', string = "Ship To")
	payment_method = fields.Selection([('check','Check'),('money_order','Money order')],"Payment Method")
	shipping_method = fields.Selection([('dhl','DHL'),('United_Parcel_Service ','United Parcel Service')],"Shipping Method")



		

