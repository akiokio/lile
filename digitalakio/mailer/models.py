from django.db import models


class CreationMixin(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Lead(CreationMixin):
	email = models.EmailField(max_length=254, unique=True, primary_key=True)
	first_name = models.CharField(max_length=254)
	last_name = models.CharField(max_length=254)

	def __unicode__(self):
		return self.email


class Email(CreationMixin):
	title = models.CharField(max_length=500)
	content = models.TextField()
	plain_content = models.TextField()

	def __unicode__(self):
		return self.title

class Queue(CreationMixin):
	title = models.CharField(max_length=254)

	email = models.ForeignKey(Email)
	recipients = models.ManyToManyField(Lead, through='LeadContact')

	def __unicode__(self):
		return self.title


class LeadContact(CreationMixin):
	PENDING = 1
	SENT = 2
	BOUNCED = 3
	OPENED = 4

	LEAD_CONTACT_STATUS = (
		(PENDING, 'Pending'),
		(SENT, 'Sent'),
		(BOUNCED, 'Bounced'),
		(OPENED, 'Opened')
	)

	queue = models.ForeignKey(Queue)
	recipient = models.ForeignKey(Lead)

	status = models.CharField(max_length=254, choices=LEAD_CONTACT_STATUS)

	def __unicode__(self):
		return '%s - %s' % (self.queue, self.recipient)
