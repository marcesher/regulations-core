# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    """The purpose of this migration is to enforce the correct character set
    and collation in mysql databases. We need utf8 to encode certain,
    non-latin characters and we need a case-sensitive collation so that we
    might have both 1005-A-b and 1005-A-B."""

    def _longtext(self, table, field):
        sql = ('ALTER TABLE regcore_%s MODIFY %s LONGTEXT '
               + 'CHARACTER SET utf8 COLLATE utf8_bin')
        db.execute(sql % (table, field))

    def _varchar(self, table, field, length):
        sql = ('ALTER TABLE regcore_%s MODIFY %s VARCHAR(%d) '
               + 'CHARACTER SET utf8 COLLATE utf8_bin')
        db.execute(sql % (table, field, length))

    def forwards(self, orm):
        if db.backend_name == 'mysql':
            table = 'diff'
            self._varchar(table, 'old_version', 20)
            self._varchar(table, 'new_version', 20)
            self._varchar(table, 'label', 50)
            self._longtext(table, 'diff')

            table = 'layer'
            self._varchar(table, 'version', 20)
            self._varchar(table, 'name', 20)
            self._varchar(table, 'label', 50)
            self._longtext(table, 'layer')

            table = 'notice'
            self._longtext(table, 'notice')

            table = 'regulation'
            self._varchar(table, 'version', 20)
            self._varchar(table, 'label_string', 50)
            self._longtext(table, 'text')
            self._longtext(table, 'title')
            self._longtext(table, 'children')

    models = {
        u'regcore.diff': {
            'Meta': {'unique_together': "(('label', 'old_version', 'new_version'),)", 'object_name': 'Diff', 'index_together': "(('label', 'old_version', 'new_version'),)"},
            'diff': ('regcore.fields.CompressedJSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'new_version': ('django.db.models.fields.SlugField', [], {'max_length': '20'}),
            'old_version': ('django.db.models.fields.SlugField', [], {'max_length': '20'})
        },
        u'regcore.layer': {
            'Meta': {'unique_together': "(('version', 'name', 'label'),)", 'object_name': 'Layer', 'index_together': "(('version', 'name', 'label'),)"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'layer': ('regcore.fields.CompressedJSONField', [], {}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '20'}),
            'version': ('django.db.models.fields.SlugField', [], {'max_length': '20'})
        },
        u'regcore.notice': {
            'Meta': {'object_name': 'Notice'},
            'cfr_part': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'document_number': ('django.db.models.fields.SlugField', [], {'max_length': '20', 'primary_key': 'True'}),
            'effective_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fr_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notice': ('regcore.fields.CompressedJSONField', [], {}),
            'publication_date': ('django.db.models.fields.DateField', [], {})
        },
        u'regcore.regulation': {
            'Meta': {'unique_together': "(('version', 'label_string'),)", 'object_name': 'Regulation', 'index_together': "(('version', 'label_string'),)"},
            'children': ('regcore.fields.CompressedJSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_string': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'node_type': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.SlugField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['regcore']
