import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from legacy.models import Person, Comment
class LegacyViewTests(TestCase):
    def test_comments_view(self):
        person = Person(user='1')
        person.save()

        comment = Comment(owner=person,text="This guy sucks",upvotes='3',downvotes='1')
        comment.save()

        comment = Comment(owner=person,text="This guy rocks", upvotes='6',downvotes='2')
        comment.save()

        comments=self.client.get(reverse('persons:comments', args=(person.user,))).context['comments']
        self.assertEqual(comments[0].owner, person)
        self.assertEqual(comments[0].text,"This guy sucks")
        self.assertEqual(comments[0].upvotes,3)
        self.assertEqual(comments[0].downvotes,1)

        self.assertEqual(comments[1].owner, person)
        self.assertEqual(comments[1].text, "This guy rocks")
        self.assertEqual(comments[1].upvotes,6)
        self.assertEqual(comments[1].downvotes,2)

    def test_add_view(self):
        person = Person(user='2')
        person.save()

        response = self.client.post(reverse('persons:add', args=(person.user,)), {'text':'This guy is pretty ok'})

        self.assertEqual(response.status_code,302)
        comments = Person.objects.get(user='2').comment_set.all()
        self.assertEqual(comments[0].owner,person)
        self.assertEqual(comments[0].text,'This guy is pretty ok')
        self.assertEqual(comments[0].upvotes,0)
        self.assertEqual(comments[0].downvotes,0)

    def test_vote_view(self):
        person = Person(user='3')
        person.save()

        comment = Comment(owner=person,text="blah blah blah")
        comment.save()
        response = self.client.post(reverse('persons:vote', args=(comment.pk,)),{'vote':'up','user_id':'3'})
        state = json.loads(response.content)
        self.assertEqual(state['up_change'],1)
        self.assertEqual(state['down_change'],0)

        person = Person.objects.get(user='3')
        comment = Comment.objects.get(text="blah blah blah")
        self.assertEqual(comment.upvotes,1)
        self.assertEqual(comment.downvotes,0)
        self.assertIn(comment, person.upvotes.all())
        
        response = self.client.post(reverse('persons:vote', args=(comment.pk,)),{'vote':'down','user_id':'3'})
        state = json.loads(response.content)
        self.assertEqual(state['down_change'],1)
        self.assertEqual(state['up_change'],-1)

        person = Person.objects.get(user='3')
        comment = Comment.objects.get(text="blah blah blah")
        self.assertEqual(comment.upvotes,0)
        self.assertEqual(comment.downvotes,1)
        self.assertIn(comment,person.downvotes.all())
        self.assertNotIn(comment, person.upvotes.all())
