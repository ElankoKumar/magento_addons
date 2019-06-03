from odoo import models,fields,api
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ProductsTemplate(models.Model):
	_inherit = 'product.template'
	_description = 'Magento Products'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")


	# @api.model
	# def create(self,vals):
	# 	users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
	# 	for user in users:
	# 		token = user.company_id.token
	# 		url = user.company_id.magento_url
	# 		if user.company_id.trigger == 'create' or user.company_id.trigger == 'create_or_edit':
	# 			final_url = "%sindex.php/rest/V1/products" %(url)
	# 			headers = {"Content-Type":"application/json", "Authorization":"Bearer "+token}
	# 			data = '{"product":{"name": "%s","sku":"%s","price":%d,"attribute_set_id": 4,""media_gallery_entries"":[{"content":{"base64EncodedData":%s}}]}}' %(vals.get('name'),vals.get('name'),vals.get('list_price'),vals.get('image'))
	# 			response = requests.request("POST", final_url, data=data, headers=headers)
	# 			_logger.error(response.text)
	# 			if response.status_code == 200:
	# 				_logger.error(">>>> Product Created >>>>>>")
	# 				decoded = json.loads(response.text)
	# 				vals['magento_id'] = decoded['id']
	# 				vals['is_magento'] = True
					
	# 	record = super(ProductsTemplate, self).create(vals)
	# 	return record


		

