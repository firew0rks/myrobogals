from django.conf.urls import url, include, i18n
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.static import serve as static_serve_view
from tinymce import urls as tinymce_urls

from myrobogals import settings
from myrobogals.rgchapter import views as rgchapter_views
from myrobogals.rgconf import views as rgconf_views
from myrobogals.rgmain import views as rgmain_views
from myrobogals.rgmessages import views as rgmessages_views
from myrobogals.rgprofile.views import profile_chapter, profile_user, profile_login

from myrobogals.rgweb import views as rgweb_views
from myrobogals.rgprofile.forms import PasswordResetForm, SetPasswordFrom



urlpatterns = [
	# Home
	url(r'^$', rgmain_views.home),

	# User functions
	url(r'^login/$', profile_login.show_login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^chpass/$', auth_views.password_change, {'template_name': 'password_change_form.html', 'post_change_redirect': '/profile'}),
	url(r'^forgotpass/done/$', auth_views.password_reset_done, {'template_name': 'password_reset_done_v2.html'}, name='password_reset_done'),
	url(r'^forgotpass/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'password_reset_confirm_v2.html', 'set_password_form': SetPasswordFrom}),
	url(r'^forgotpass/complete/$', auth_views.password_reset_complete, {'template_name': 'password_reset_complete_v2.html'}, name='password_reset_complete'),
	url(r'^forgotpass/$', auth_views.password_reset, {'template_name': 'password_reset_form_v2.html', 'email_template_name': 'password_reset_email.html', 'password_reset_form': PasswordResetForm}),
	#url(r'^unsubscribe/(?P<uidb36>.+)/(?P<token>.+)/(?P<step>\d)/$', auth_views.unsubscribe),
	url(r'^join/$', rgchapter_views.joinlist),
	url(r'^join/(?P<chapterurl>.+)/$', profile_user.joinchapter),
	url(r'^welcome/(?P<chapterurl>.+)/$', rgmain_views.welcome),
	url(r'^code/$', profile_login.codeofconduct),
	url(r'^code/help/$', profile_user.conduct_help),

	# Profile menu
	url(r'^profile/$', profile_user.redirtoself, name='profile'),
	url(r'^profile/contactdirectory/$', profile_chapter.contactdirectory),
	url(r'^profile/edit/$', profile_user.redirtoeditself),
	url(r'^profile/mobverify/$', profile_user.mobverify),
	#url(r'^profile/(?P<username>.+)/edit/profileimage/$', 'profileimages.views.upload_profile_image'),
	url(r'^profile/(?P<username>.+)/edit/$', profile_user.edituser),
	url(r'^profile/(?P<username>.+)/genpw/$', profile_user.genpw),
	url(r'^profile/(?P<username>.+)/$', profile_user.detail),

	# Conferences submenu
	url(r'^conferences/$', rgconf_views.home),
	url(r'^conferences/(?P<conf_id>\d+)/$', rgconf_views.rsvplist),
	url(r'^conferences/(?P<conf_id>\d+)/nametags\.csv$', rgconf_views.nametagscsv),
	url(r'^conferences/(?P<conf_id>\d+)/email/$', rgconf_views.rsvpemail),
	url(r'^conferences/(?P<conf_id>\d+)/(?P<username>.+)/rsvp/$', rgconf_views.editrsvp),
	url(r'^conferences/(?P<conf_id>\d+)/(?P<username>.+)/invoice/$', rgconf_views.showinvoice),

	# Forums
	url(r'^forums/', include('myrobogals.rgforums.urls')),

	# Chapters menu
	url(r'^chapters/', include('myrobogals.rgchapter.urls', namespace='chapters')),

	# Workshops menu
	url(r'^teaching/', include('myrobogals.rgteaching.urls', namespace='teaching')),

	# Reporting metrics
	url(r'^reports/', include('myrobogals.rgreport.urls', namespace='reports')),

	# Email & SMS menu
	url(r'^messages/img/(?P<msgid>\d+)/(?P<filename>.+)$', rgmessages_views.serveimg),
	url(r'^messages/(?P<msgid>\d+)/(?P<issue>.+)/$', rgmessages_views.servenewsletter),
	url(r'^messages/sms/write/$', rgmessages_views.writesms),
	url(r'^messages/sms/done/$', rgmessages_views.smsdone),
	url(r'^messages/sms/overlimit/$', rgmessages_views.smsoverlimit),
	url(r'^messages/email/write/$', rgmessages_views.writeemail),
	url(r'^messages/setmaxuploadfilesize/$', rgmessages_views.setmaxuploadfilesize),
	url(r'^messages/email/done/$', rgmessages_views.emaildone),
	url(r'^messages/newsletters/(?P<newsletter_id>\d+)/$', rgmessages_views.newslettercp),
	url(r'^messages/newsletters/(?P<newsletter_id>\d+)/import/$', rgmessages_views.importsubscribers),
	url(r'^messages/newsletters/(?P<newsletter_id>\d+)/import/help/$', rgmessages_views.importsubscribershelp),
	url(r'^messages/emailrecipients/(?P<email_id>\d+)/$', rgmessages_views.emailrecipients),
	url(r'^messages/smsrecipients/(?P<sms_id>\d+)/$', rgmessages_views.smsrecipients),
	url(r'^messages/showemail/(?P<email_id>\d+)/$', rgmessages_views.showemail),
	url(r'^messages/downloademailfile/(?P<email_id>\d+)/(?P<file_name>.+)/$', rgmessages_views.downloademailfile),
	url(r'^messages/history/$', rgmessages_views.msghistory),
	url(r'^messages/previewemail/$', rgmessages_views.previewemail),
	
	# Changelogs
	url(r'^changelogs/$', rgmain_views.changelogs),

	# Wiki
	url(r'^wiki/', include('myrobogals.rgwiki.urls', namespace='wiki')),
	url(r'^markdownx/', include('markdownx.urls')),

	# Static pages
	url(r'^credits/$', rgmain_views.credits),
	url(r'^support/$', rgmain_views.support),

	# Careers newsletter API
	url(r'^api/newslettercareers/$', rgmessages_views.careersapi),
	# Amplifier newsletter API
	url(r'^api/newsletter/$', rgmessages_views.api),
	# SMSGlobal delivery receipts API
	url(r'^api/dlr/$', rgmessages_views.dlrapi),
	# Google Maps KML API
	url(r'^api/chapter-map.kml', rgchapter_views.chaptermap),
	# Delete user API
	url(r'^delete/user/(?P<userpk>\d+)/$', profile_chapter.deleteuser),

	# i18n helpers
	url(r'^i18n/', include(i18n)),
	# TinyMCE helpers
	url(r'^tinymce/', include(tinymce_urls)),
	
	# Admin site
	url(r'^topsecretarea/', include(admin.site.urls)),
]

# If running the local development server - this will serve the media files through it too
if settings.DEBUG:
	urlpatterns.append(url(r'^rgmedia/(?P<path>.*)$', static_serve_view, {'document_root': settings.MEDIA_ROOT}))

# Custom view for 500 Internal Server Error
handler500 = 'myrobogals.rgmain.views.servererror'

