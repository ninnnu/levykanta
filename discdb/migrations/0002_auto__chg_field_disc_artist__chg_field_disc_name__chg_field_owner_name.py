# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Disc.artist'
        db.alter_column('discdb_disc', 'artist', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Disc.name'
        db.alter_column('discdb_disc', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Owner.name'
        db.alter_column('discdb_owner', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Wish.source'
        db.alter_column('discdb_wish', 'source', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Track.artist'
        db.alter_column('discdb_track', 'artist', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Track.name'
        db.alter_column('discdb_track', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))


    def backwards(self, orm):
        
        # Changing field 'Disc.artist'
        db.alter_column('discdb_disc', 'artist', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Disc.name'
        db.alter_column('discdb_disc', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Owner.name'
        db.alter_column('discdb_owner', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Wish.source'
        db.alter_column('discdb_wish', 'source', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Track.artist'
        db.alter_column('discdb_track', 'artist', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Track.name'
        db.alter_column('discdb_track', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))


    models = {
        'discdb.disc': {
            'Meta': {'object_name': 'Disc'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['discdb.Owner']"}),
            'returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tracks'", 'blank': 'True', 'db_table': "'Discs_to_Tracks'", 'to': "orm['discdb.Track']"})
        },
        'discdb.owner': {
            'Meta': {'object_name': 'Owner'},
            'discs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'discs'", 'blank': 'True', 'to': "orm['discdb.Disc']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'discdb.track': {
            'Meta': {'object_name': 'Track'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'disc': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['discdb.Disc']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'discdb.wish': {
            'Meta': {'object_name': 'Wish'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'track': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['discdb']
