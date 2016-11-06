# coding: utf-8

from controller import Controller

class PID(Controller):
	
	def __init__(self):
		super(PID, self).__init__()
		
		#define this in JSON
		self._Kp = 6.0
		self._Ki = 0.0
		self._Kd = 1.0
		self._dt = 1

		self._inter = 0.0
		self._error = 0.0;
		
	def run(self, error):
		self._inter += error * self._dt
		#TODO boundary check for intergral term
		diff = (error - self._error) / self._dt
		self._error = error
	
		pid = self._Kp * error + self._Ki * self._inter + self._Kd * diff

		return pid

	def reset(self):	
		self.inter = 0;
		self._error = 0;
		
