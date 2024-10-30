# -*- coding: utf-8 -*-
# from odoo import http


# class PosNcdTracking(http.Controller):
#     @http.route('/pos_ncd_tracking/pos_ncd_tracking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_ncd_tracking/pos_ncd_tracking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_ncd_tracking.listing', {
#             'root': '/pos_ncd_tracking/pos_ncd_tracking',
#             'objects': http.request.env['pos_ncd_tracking.pos_ncd_tracking'].search([]),
#         })

#     @http.route('/pos_ncd_tracking/pos_ncd_tracking/objects/<model("pos_ncd_tracking.pos_ncd_tracking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_ncd_tracking.object', {
#             'object': obj
#         })

