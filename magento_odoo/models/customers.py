from odoo import models,fields,api
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ResCustomers(models.Model):
	_inherit = 'res.partner'


	magento_id = fields.Char("Magento ID")
	is_magento = fields.Boolean("Magento ?")



	# @api.model
	# def create(self,vals):
	# 	print(vals.get('image'))
	# 	users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
	# 	name = vals.get('name')
	# 	rec = {}
	# 	cnt = name.split(" ")
	# 	if(len(cnt)>1):
	# 		rec['firstname'] = cnt[0]
	# 		rec['lastname'] = cnt[1]
	# 	else:
	# 		rec['firstname'] = name
	# 		rec['lastname'] = name
	# 	rec['email'] = vals.get('email')
	# 	final_rec = {}
	# 	final_rec['customer'] = rec
	# 	# rec['is_magento'] = True

	# 	for user in users:
	# 		url = user.company_id.magento_url
	# 		final_url = "%sindex.php/rest/V1/customers" %(url)
	# 		data = json.dumps(final_rec)
	# 		headers = {"Content-Type":"application/json"}
	# 		response = requests.request("POST", final_url, data=data, headers=headers)
	# 		_logger.error(response.text)
	# 		if response.status_code == 200:
	# 			decoded = json.loads(response.text)
	# 			vals['is_magento'] = True
	# 			vals['magento_id'] = decoded['id']
	# 	record = super(ResCustomers, self).create(vals)
	# 	# update_rec = self.env['res.partner'].search([('id','=',record.id)],limit=1)
	# 	# update_rec.write({'is_magento':True,'magento_id':response['id']})
	# 	return record




class ResCompany(models.Model):
	_inherit = 'res.company'

	username = fields.Char("Magento username")
	password = fields.Char("Magento password")
	magento_url = fields.Char("Magento URL")
	token = fields.Char("Token")
	logfile_path = fields.Char("Log File Path")
	import_customer = fields.Boolean("Import Customers")
	export_customers = fields.Boolean("Export Customers")
	import_products = fields.Boolean("Import Products")
	export_products = fields.Boolean("Export Products")
	import_orders = fields.Boolean("Import Orders")
	export_orders = fields.Boolean("Export Orders")
	import_invoices = fields.Boolean("Import Invoices")
	export_invoices = fields.Boolean("Export Invoices")
	import_categories = fields.Boolean("Import Categories")
	export_categories = fields.Boolean("Export Categories")
	auto_sync = fields.Selection([('yes','Yes'),('no','No')],"Auto Sync ?")
	trigger = fields.Selection([('create','Create'),('edit','Edit'),('create_or_edit','Create or Edit'),('none','None')],string = "Triggers")

	
	@api.multi
	def authenticate_magento(self):
		print("It is Authenticated")
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			username = user.company_id.username
			password= user.company_id.password
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/integration/admin/token" %(url)
			data = '{"username" : "'+username+'","password" : "'+password+'"}'
			headers = {"Content-Type":"application/json"}
			response = requests.request("POST", final_url, data=data, headers=headers)
			code = response.text
			code = code.replace('"','')
			user.company_id.sudo().write({'token':code})
			# self.token = code
			_logger.error("AuthToken Generated >>>>>>>>>>>>>>>")

	@api.multi
	def check_cron_jobs(self):
		print("??????????????????????????")
		print("cron Job is Working")
		return "Cron Job"



	@api.multi
	def get_customers(self):
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			token = user.company_id.token
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/products?searchCriteria=null" %(url)
			headers = {"Authorization":"Bearer "+token}
			response = requests.get(final_url, headers=headers)
			print(response.text)

	@api.multi
	def get_logging(self):
		filepath = self.logfile_path
		# filepath = 'Iliad.txt'  
		with open(filepath) as fp:  
		   line = fp.readline()
		   cnt = 1
		   while line:
			   print("Line {}: {}".format(cnt, line.strip()))
			   line = fp.readline()
			   cnt += 1



	@api.multi
	def import_customers_magento(self):
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			token = user.company_id.token
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/customers?searchCriteria=null" %(url)
			headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
			response = requests.get(final_url, headers=headers)
			_logger.error(response.text)
			if response.status_code == 200:
				decoded = json.loads(response.text)
				print(decoded)
			
			
	@api.multi
	def import_products_magento(self):
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			token = user.company_id.token
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/products?searchCriteria=null" %(url)
			headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
			response = requests.get(final_url, headers=headers)
			_logger.error(response.text)
			if response.status_code == 200:
				decoded = json.loads(response.text)
				items = decoded['items']
				for item in items:
					print(item)
					if item.get('id'):
						product = self.env['product.template'].search([('magento_id','=',item.get('id'))],limit=1)
						if not product:
							product_vals = {}
							product_vals['name'] = item.get('name')
							product_vals['list_price'] = item.get('price')
							product_vals['magento_id'] = item.get('id')
							product_vals['is_magento'] = True
							create_product = self.env['product.template'].create(product_vals)
							_logger.error("Product Created"+str(create_product.id))
						else:
							print("****************************************")
							print("Product Exists")


	@api.multi
	def export_products_magento(self):
		products = self.env['product.template'].search(['&',('is_magento','=',True),('magento_id','=',False)])
		for product in products:
			data = '{"product":{"name": "%s","sku":"%s","price":%d, "attribute_set_id": 4}}' %(product.name, product.name, product.list_price)
			#print(data)
			users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
			for user in users:
				url = user.company_id.magento_url
				token = user.company_id.token
				final_url = "%sindex.php/rest/V1/products" %(url)
				# data = json.dumps(final_rec)
				headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
				response = requests.request("POST", final_url, data=data, headers=headers)
				# _logger.error(response.text)
				sku = False
				if response.status_code == 200:
					vals = {}
					decoded = json.loads(response.text)
					vals['is_magento'] = True
					vals['magento_id'] = decoded.get('id')
					sku = decoded.get('sku')
				if sku:
					put_url = "%sindex.php/rest/V1/products/%s" %(url,sku)
					headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
					put_response = requests.request("PUT", put_url, data=data, headers=headers)
					_logger.error(put_response.text)
				product.write(vals)




	@api.multi
	def import_customers_magento(self):
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			token = user.company_id.token
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/customers/search?searchCriteria=null" %(url)
			headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
			response = requests.get(final_url, headers=headers)
			# _logger.error(response.text)
			if response.status_code == 200:
				decoded_data = json.loads(response.text)
				items = decoded_data['items']
				for item in items:
					if item.get('id'):
						customer = self.env['res.partner'].search([('magento_id','=',item.get('id'))])
						if not customer:
							vals = {}
							vals['name'] = item.get('firstname') + ' ' + item.get('lastname')
							vals['magento_id'] = item.get('id')
							vals['is_magento'] = True
							vals['email'] = item.get('email')
							vals['customer'] = True
							create_customer = self.env['res.partner'].create(vals)
							_logger.error("Customer Created : "+str(create_customer.id))
						else:
							_logger.error("Customer already Exists")


	@api.multi
	def export_customer_magento(self):
		# print("Customer Exported")
		customers = self.env['res.partner'].search(['&',('is_magento','=',True),('magento_id','=',False)])
		for customer in customers:
			name = customer.name
			rec = {}
			cnt = name.split(" ")
			if(len(cnt)>1):
				rec['firstname'] = cnt[0]
				rec['lastname'] = cnt[1]
			else:
				rec['firstname'] = name
				rec['lastname'] = name
			rec['email'] = customer.email
			final_rec = {}
			final_rec['customer'] = rec
			users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
			for user in users:
				url = user.company_id.magento_url
				final_url = "%sindex.php/rest/V1/customers" %(url)
				data = json.dumps(final_rec)
				headers = {"Content-Type":"application/json"}
				response = requests.request("POST", final_url, data=data, headers=headers)
				_logger.error(response.text)
				if response.status_code == 200:
					vals = {}
					decoded = json.loads(response.text)
					vals['is_magento'] = True
					vals['magento_id'] = decoded['id']
				customer.write(vals)



	@api.multi
	def import_sale_orders_magento(self):
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			token = user.company_id.token
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/orders?searchCriteria=null" %(url)
			headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
			response = requests.get(final_url, headers=headers)
			if response.status_code == 200:
				decoded_data = json.loads(response.text)
				items = decoded_data.get('items')
				for item in items:
					customer_id = item.get('customer_id')
					grand_total = item.get('base_grand_total')
					shipping = item.get('base_shipping_invoiced')
					amount_total = item.get('base_grand_total')
					untaxed_amount = item.get('base_subtotal_incl_tax')
					order_state = item.get('state')
					check_id = item.get('entity_id')
					order_check = self.env['sale.order'].search([('magento_id','=',check_id)],limit=1)
					if not order_check:
						if customer_id:
							partners = self.env['res.partner'].search([('magento_id','=',customer_id)],limit=1)
							for partner in partners:
								vals = {}
								vals['partner_id'] = partner.id
								vals['is_magento'] = True
								# vals['magento_id'] = 2
								vals['amount_total'] = grand_total
								vals['shipping_charge'] = shipping
								vals['amount_untaxed'] = untaxed_amount
								create_order = self.env['sale.order'].create(vals)
								_logger.error("Order Created : "+str(create_order.id))
								order_id = create_order.id
								# create_order.write({'state':'sale'})
								print("Sale Order State : "+create_order.state)
								products = item.get('items')
								for product in products:
									product_id = product.get('product_id')
									qty = product.get('qty_ordered')
									# price = product.get('price')
									odoo_products = self.env['product.template'].search([('magento_id','=',product_id)])
									if odoo_products:
										for pro in odoo_products:
											product_lines = self.env['product.product'].search([('product_tmpl_id','=',pro.id)],limit=1)
											if product_lines:
												for line in product_lines:
													price = line.lst_price
													od_product_id = line.id
													line_vals = {}
													line_vals['order_id'] = order_id
													line_vals['product_id'] = od_product_id
													line_vals['product_uom_qty'] = qty
													line_vals['price_unit'] = price
													line_vals['tax_id'] = False
													line_vals['customer_lead'] = 0.0
													line_create = self.env['sale.order.line'].create(line_vals)
													create_order.write({'magento_id':product.get('order_id')})
													_logger.error("Line Created : "+str(line_create.id))

								if order_state == 'new':
									create_order.sudo().write({'state':'draft'})
								elif order_state == 'complete':
									create_order.sudo().write({'state':'sale'})
								elif order_state == 'canceled':
									create_order.sudo().write({'state':'cancel'})
					else:
						_logger.error("Order exists Already >>>>> ")


	@api.multi
	def import_mg_categories(self):
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			token = user.company_id.token
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/categories" %(url)
			headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
			response = requests.get(final_url, headers=headers)
			if response.status_code == 200:
				decoded_data = json.loads(response.text)
				category_check = self.env['product.category'].search([('magento_id','=',decoded_data.get('id'))])
				_logger.error(decoded_data)
				if not category_check:	
					vals = {}
					vals['name'] = decoded_data.get('name')
					vals['magento_id'] = decoded_data.get('id')
					vals['is_magento'] = True
					category_create = self.env['product.category'].create(vals)
					_logger.error("Category Created : "+str(category_create.id))
				
				else:
					_logger.error("Category Exists .... ")

	

	@api.multi
	def import_invoices_magento(self):
		users = self.env['res.users'].search([('id','=',self.env.uid)],limit=1)
		for user in users:
			token = user.company_id.token
			url = user.company_id.magento_url
			final_url = "%sindex.php/rest/V1/invoices?searchCriteria=null" %(url)
			headers = {"Authorization":"Bearer "+token,"Content-Type":"application/json"}
			response = requests.get(final_url, headers=headers)
			# _logger.error(response.text)
			if response.status_code == 200:
				decoded_data = json.loads(response.text)
				items = decoded_data.get('items')
				for item in items:
					order_id = item.get('order_id')
					orders = self.env['sale.order'].search([('magento_id','=',order_id)],limit=1)
					if orders:
						customer_rec = orders[0]['partner_id']
						source_doc = orders[0]['']
						customer_id = customer_rec.id
						vals = {}
						vals['partner_id'] = customer_id
						vals['is_magento'] = True
						vals['magento_id'] = item.get('id')
						create_invoice = self.env['account.invoice'].create(vals)
						_logger.error("Invoice Created : "+str(create_invoice.id))
						if create_invoice:
							invoice_id = create_invoice.id
							product_lines = item.get('items')
							for product in product_lines:
								product_id = product.get('product_id')
								product_temp = self.env['product.product'].search([('magento_id','=',product_id)],limit=1)
								if product_temp:
									product_vals = {}
									product_vals['invoice_id'] = invoice_id
									product_vals['product_id'] = product_temp.id
									product_vals['name'] = product_temp.name
									product_vals['quantity'] = product.get('qty')
									product_vals['price_unit'] = product_temp.lst_price
									product_vals['invoice_line_tax_ids'] = False
									product_vals['account_id'] = 3
									create_lines = self.env['account.invoice.line'].sudo().create(product_vals)
									_logger.error("Invoice Lines Created : "+str(create_lines.id))