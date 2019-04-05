# -*- coding: utf-8 -*-
from openerp import models, fields
from openerp.addons import decimal_precision as dp
class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    short_name = fields.Char('Short Title',size=5,)
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner',string='Authors')
    reader_rating = fields.Float(
                                'Reader Average Rating',
                                (3, 2), # Optional precision (total, decimals),
                                )
    cost_price = fields.Float("Book Cost", dp.get_precision('Book Price'))

    def name_get(self):
        result = []
        for record in self:
            result.append(
            (record.id,u"%s (%s)" % (record.name, record.date_release)))
        return result