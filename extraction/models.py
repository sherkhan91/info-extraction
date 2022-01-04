from django.db import models

# Create your models here.
class Publication(models.Model):
	name = models.CharField(null=False, blank=False, max_length=200)
	pubcode = models.CharField(null=False, blank=False, max_length=200, unique=True)
	# publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
	publisher = models.CharField(null=False, blank=False, max_length=200)
	live = models.BooleanField(null=False, blank=False, default=False)
	asin = models.CharField(null=True, blank=True, max_length=200, unique=False, default=False)
	repub = models.BooleanField(default=True)
	amazon = models.BooleanField(default=False)
	kindle = models.BooleanField(default=False)
	pmg = models.BooleanField(default=False)
	recipe = models.BooleanField(default=False)
	puzzle = models.BooleanField(default=False)
	extra_xml = models.BooleanField(default=False)
	repub_new = models.BooleanField(default=True)
	priority = models.BooleanField(default=True)
	frequency = models.CharField(null=True, blank=True, max_length=200, default=None)
	feed_time = models.TimeField(null=True, blank=True)
	avg_page_count = models.IntegerField(null=True, blank=True)
	
	contractor = models.CharField(null=True, blank=True, max_length=200, default=None)
	ftp_client_in = models.CharField(null=True, blank=True, max_length=200, default=None)
	ftp_client_out = models.CharField(null=True, blank=True, max_length=200, default=None)
	ftp_contractor_in = models.CharField(null=True, blank=True, max_length=200, default=None)
	ftp_contractor_out = models.CharField(null=True, blank=True, max_length=200, default=None)

	def __str__(self):
		return self.name

	# contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
	# ftp_client_in = models.ForeignKey(FtpServer, models.CASCADE, related_name='ftp_client_in', null=True)
	# ftp_client_out = models.ManyToManyField(FtpServer, related_name='ftp_client_out', blank=True)
	# ftp_contractor_in = models.ForeignKey(FtpServer, models.CASCADE, related_name='ftp_contractor_in', null=True)
	# ftp_contractor_out = models.ForeignKey(FtpServer, models.CASCADE, related_name='ftp_contractor_out', null=True)




class Edition(models.Model):
	UNKNOWN = 0
	RECEIVECLIENT = 1
	SENDCONTR = 2
	RECEIVECONTR = 3
	SENDCLIENT = 4
	COMPLETED = 5
	issuestatus = [(0, 'Unknown'),
			   	(1, 'To receive from client'),
			   	(2, 'To send to contractor'),
			   	(3, 'To receive from contractor'),
			   	(4, 'To send to client'),
			   	(5, 'Completed'), ]
 
	NOMAIL = 0
	MINUSTHREE = 1
	MINUSTWO = 2
	MINUSONE = 3
	ZERODAY = 4
	ZERODAY30 = 5
	ZERODAY120 = 6
	PLUSONE = 7
	PLUSTWO = 8
	IGNORE = 9
	INCORRECT = 10
	HOLD = 20
	mailstatus = [(20, 'Feed hold (awaiting release) notification sent.'),
			  	(0, 'No mails sent'),
				  (1, '-3 day feed notification sent'),
			  	(2, '-2 day feed notification sent'),
			  	(3, '-1 day feed notification sent'),
			  	(4, '0 day feed notification sent'),
			  	(5, '0+30mins day feed notification sent'),
			  	(6, '0+120mins day feed notification sent'),
			  	(7, '+1 day feed notification sent'),
			  	(8, '+2 day feed notification sent'),
			  	(9, 'Notification sent feed will go on ignore list'),
			  	(10, 'Incorrect feed notification sent'), ]
 
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
	issue = models.CharField(null=False, blank=False, max_length=200)
	issue_id = models.CharField(null=True, blank=True, max_length=200)
	pages = models.IntegerField(null=True, blank=True)
	processed_pages = models.IntegerField(null=True, blank=True)
	processed_pages_repub = models.IntegerField(null=True, blank=True)
	processed_pages_adv = models.IntegerField(null=True, blank=True)
	via_repub2qa = models.BooleanField(default=False)
	expected = models.DateField(null=True, blank=True, max_length=200)
	client_received = models.DateTimeField(null=True, blank=True)
	contractor_sent = models.DateTimeField(null=True, blank=True)
	contractor_received = models.DateTimeField(null=True, blank=True)
	client_sent = models.DateTimeField(null=True, blank=True)
	sent_to = models.CharField(null=True, blank=True, max_length=200, default='Dummy value')
	ftp_sent_to = models.CharField(null=True, blank=True, max_length=200, default='Dummy Value')
	# sent_to = models.ManyToManyField(Client, blank=True)
	# ftp_sent_to = models.ManyToManyField(FtpServer, blank=True)
	invoice_client = models.CharField(null=True, blank=True, max_length=200, default='repubqa')
	invoice_contractor = models.CharField(null=True, blank=True, max_length=200)
	ignore = models.BooleanField(default=False)
	status = models.PositiveSmallIntegerField(choices=issuestatus, default=0)
	mailstatus = models.PositiveSmallIntegerField(choices=mailstatus, default=0)


class Notes(models.Model):
	note = models.TextField(null=True, blank=True, default=None)
	internal = models.BooleanField(null=True, blank=True, default=None)
	date_created = models.DateTimeField(auto_now_add=True, editable=False)
	date_modified = models.DateTimeField(auto_now=True, editable=False)
	edition = models.ForeignKey(Edition, on_delete=models.CASCADE, null=True, blank=True)
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE,null=True, blank=True)

