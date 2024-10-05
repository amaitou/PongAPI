from .utils import Utils
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import status
from django.conf import settings

class CookieTokenAuthentication:

	def __init__(self, get_response):
		self.get_response = get_response

	
	def __generate_error_response(self, message: str, redirect: bool, redirect_url: str) -> Response:
		response = Response({
			'error': message,
		},
		status=status.HTTP_401_UNAUTHORIZED)
		response.accepted_renderer = JSONRenderer()
		response.accepted_media_type = 'application/json'
		response.renderer_context = {}
		response.render()

		response.delete_cookie(settings.ACCESS_TOKEN)
		response.delete_cookie(settings.REFRESH_TOKEN)

		return response
	
	def __call__(self, request):

		access_token = request.COOKIES.get(settings.ACCESS_TOKEN)

		if not access_token:
			return self.get_response(request)
		
		try:
			user = Utils.get_user_from_jwt(access_token, 'access')
			if not user:
				raise Exception('Invalid access token')
		except Exception as e:
			refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN)
			if not refresh_token:
				return self.__generate_error_response('No refresh token was provided', 
						True, 
						'/api/login/')

			try:
				old_refresh_token = RefreshToken(refresh_token)
			except TokenError as e:
				return self.__generate_error_response('Invalid or Expired refresh token',
										True,
										'/api/login/')
			
			user = Utils.get_user_from_jwt(refresh_token, 'refresh')
			old_refresh_token.blacklist()

			tokens = Utils.create_jwt_for_user(user)

			if not user:
				return self.__generate_error_response('Failed to find user',
										True,
										'/api/login/')
			
			request.COOKIES[settings.ACCESS_TOKEN] = str(tokens['access_token'])
			request.COOKIES[settings.REFRESH_TOKEN] = str(tokens['refresh_token'])

			response = self.get_response(request)
			response.set_cookie(settings.ACCESS_TOKEN, str(tokens['access_token']), httponly=False)
			response.set_cookie(settings.REFRESH_TOKEN, str(tokens['refresh_token']), httponly=True)

			return response
	
		request.user = user
		response = self.get_response(request)
		return response
