# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'persons_person', (
            ('user', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
        ))
        db.send_create_signal(u'persons', ['Person'])

        # Adding M2M table for field upvotes on 'Person'
        m2m_table_name = db.shorten_name(u'persons_person_upvotes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'persons.person'], null=False)),
            ('comment', models.ForeignKey(orm[u'persons.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'comment_id'])

        # Adding M2M table for field downvotes on 'Person'
        m2m_table_name = db.shorten_name(u'persons_person_downvotes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'persons.person'], null=False)),
            ('comment', models.ForeignKey(orm[u'persons.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'comment_id'])

        # Adding model 'Comment'
        db.create_table(u'persons_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Person'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('downvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'persons', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'persons_person')

        # Removing M2M table for field upvotes on 'Person'
        db.delete_table(db.shorten_name(u'persons_person_upvotes'))

        # Removing M2M table for field downvotes on 'Person'
        db.delete_table(db.shorten_name(u'persons_person_downvotes'))

        # Deleting model 'Comment'
        db.delete_table(u'persons_comment')


    models = {
        u'persons.comment': {
            'Meta': {'object_name': 'Comment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'downvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['persons.Person']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'persons.person': {
            'Meta': {'object_name': 'Person'},
            'downvotes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'downvoters'", 'symmetrical': 'False', 'to': u"orm['persons.Comment']"}),
            'upvotes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'upvoters'", 'symmetrical': 'False', 'to': u"orm['persons.Comment']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'})
        }
    }

    complete_apps = ['persons']