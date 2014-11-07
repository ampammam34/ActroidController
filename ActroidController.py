#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ActroidController.py
 @brief ModuleDescription
 @date $Date$


"""
import sys, traceback
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import csv


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
actroidcontroller_spec = ["implementation_id", "ActroidController", 
		 "type_name",         "ActroidController", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class ActroidController
# @brief ModuleDescription
# 
# 
class ActroidController(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_pose_target = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._pose_targetIn = OpenRTM_aist.InPort("pose_target", self._d_pose_target)
		self._d_pose_position = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._pose_positionIn = OpenRTM_aist.InPort("pose_position", self._d_pose_position)
		self._d_poseout = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._poseoutOut = OpenRTM_aist.OutPort("poseout", self._d_poseout)

                
		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("pose_target",self._pose_targetIn)
		self.addInPort("pose_position",self._pose_positionIn)
		
		# Set OutPort buffers
		self.addOutPort("poseout",self._poseoutOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
        #        self.f.close()
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onActivated(self, ec_id):
                self.f = open('data.csv','ab')
                self.csvWriter = csv.writer(self.f)

                self._current_pose_updated = False
                self._target_pose_updated = False
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onDeactivated(self, ec_id):
                self.f.close()
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
                try:

                        if self._pose_positionIn.isNew():
                                self._d_pose_position = self._pose_positionIn.read()                                
                                self._current_pose_updated = True       
                        if self._pose_targetIn.isNew():      
                                self._d_pose_target = self._pose_targetIn.read()
                                print self._d_pose_target
                                self._target_pose_updated = True

                        # もし両方のデータが更新されていたら
                        if self._current_pose_updated == True and self._target_pose_updated == True:
                                listData = [self._d_pose_position.data, self._d_pose_target.data]
                                self.csvWriter.writerow(listData)

                                self._d_poseout = self._d_pose_target
                                self._poseoutOut.write()

                        return RTC.RTC_OK

                except Exception, e:
                        print 'Exception : ', e
                        traceback.print_exc()
                        #これは print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback, limit, file) の省略表現
                        pass

                return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def ActroidControllerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=actroidcontroller_spec)
    manager.registerFactory(profile,
                            ActroidController,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ActroidControllerInit(manager)

    # Create a component
    comp = manager.createComponent("ActroidController")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

