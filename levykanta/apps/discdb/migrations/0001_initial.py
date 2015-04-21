# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Disc'
        db.create_table('discdb_disc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owners', to=orm['discdb.Owner'])),
            ('returned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('barcode', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
        ))
        db.send_create_signal('discdb', ['Disc'])

        # Adding M2M table for field tracks on 'Disc'
        db.create_table('Discs_to_Tracks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('disc', models.ForeignKey(orm['discdb.disc'], null=False)),
            ('track', models.ForeignKey(orm['discdb.track'], null=False))
        ))
        db.create_unique('Discs_to_Tracks', ['disc_id', 'track_id'])

        # Adding model 'Owner'
        db.create_table('discdb_owner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('discdb', ['Owner'])

        # Adding M2M table for field discs on 'Owner'
        db.create_table('discdb_owner_discs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('owner', models.ForeignKey(orm['discdb.owner'], null=False)),
            ('disc', models.ForeignKey(orm['discdb.disc'], null=False))
        ))
        db.create_unique('discdb_owner_discs', ['owner_id', 'disc_id'])

        # Adding model 'Track'
        db.create_table('discdb_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('disc', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['discdb.Disc'], null=True, blank=True)),
        ))
        db.send_create_signal('discdb', ['Track'])

        # Adding model 'Wish'
        db.create_table('discdb_wish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('track', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('discdb', ['Wish'])


    def backwards(self, orm):
        
        # Deleting model 'Disc'
        db.delete_table('discdb_disc')

        # Removing M2M table for field tracks on 'Disc'
        db.delete_table('Discs_to_Tracks')

        # Deleting model 'Owner'
        db.delete_table('discdb_owner')

        # Removing M2M table for field discs on 'Owner'
        db.delete_table('discdb_owner_discs')

        # Deleting model 'Track'
        db.delete_table('discdb_track')

        # Deleting model 'Wish'
        db.delete_table('discdb_wish')


    models = {
        'discdb.disc': {
            'Meta': {'object_name': 'Disc'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['discdb.Owner']"}),
            'returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tracks'", 'blank': 'True', 'db_table': "'Discs_to_Tracks'", 'to': "orm['discdb.Track']"})
        },
        'discdb.owner': {
            'Meta': {'object_name': 'Owner'},
            'discs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'discs'", 'blank': 'True', 'to': "orm['discdb.Disc']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'discdb.track': {
            'Meta': {'object_name': 'Track'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'disc': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['discdb.Disc']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'discdb.wish': {
            'Meta': {'object_name': 'Wish'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'track': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['discdb']
