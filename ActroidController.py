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

class RingBuffer :

        def __init__(self, num):
                self._buffer = [0.0] * num
                self._len = num
                self._counter = 0

        def length(self):
                return self._len
                
        def push(self, data):
                self._buffer[self._counter] = data
                self._counter = self._counter + 1
                if self._counter == self._len:
                        self._counter  = 0

        def pop(self):
                return self._buffer[self._counter]

        def getSum(self):
                sum = 0.0
                for data in self._buffer:
                        sum = sum + data
                return sum

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
                self.time1 = time.time()
                self.f = open('data.csv','ab')
                self.csvWriter = csv.writer(self.f)
                self._current_pose_updated = False
                self._target_pose_updated = False
                self._target = [0.0]*24 #targetの初期化
                self._current = [0.0]*24 #currentの初期化
                self._epsilon = [0.0]*24 #epsilonの初期化
                self._sum = [0.0]*24 #sumの初期化
                self._output = [0.0]*24 #outputの初期化
                self._gain = [0.0,# 1:Eyebrows up&down  
                              0.0,# 2:Eyelids open&shut 
                              0.0,# 3:Eyes right&left 
                              0.0,# 4:Eyes up&down 
                              0.0,# 5:Mouth open&shut 
                              0.0,# 6:left neck  
                              0.0,# 7:right neck  
                              0.0,# 8:Neck turning
                              0.001,# 9:left arm up       #L1 決定
                              0.005,# 10:left arm open     #L2 決定
                              0.0001,# 11:left upper arm   #L3  決定(0でも変わらん) 
                              0.00005,# 12:left elbow       #L4  決定(0でも変わらん) 
                              0.005,# 13:left forearm     #L5 超結果良い
                              0.003,# 14:left hand length #L6  決定
                              0.002,# 15:left hand side   #L7  決定
                              0.0,# 16:right arm up     #R1
                              0.0,# 17:right arm open   #R2
                              0.0,# 18:right upper arm  #R3
                              0.0,# 19:right elbow      #R4
                              0.0,# 20:right forearm    #R5
                              0.0,# 21:right hand length
                              0.0,# 22:right hand side 
                              0.0,# 23:Body front&back
                              0.0]# 24:Body turning #gainの初期化
                self._ringBuffer = []
                for i in range(24):
                        self._ringBuffer.append(RingBuffer(100))
                        
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
                        self.time2 = time.time()

                        delta_time = float(self.time2-self.time1)
                        if self._pose_positionIn.isNew():
                                data = self._pose_positionIn.read()
                                for i in range(24):
                                        self._current[i] = data.data[i]
                                #self.time = self._d_pose_position.tm.sec + (self._d_pose_position.tm.nsec / 1000000000)
                                self._current_pose_updated = True       
                        if self._pose_targetIn.isNew():
                                d = self._pose_targetIn.read()
                                for i in range(24):
                                        self._target[i] = d.data[i]
                                self.time = self._d_pose_target.tm
                                self._target_pose_updated = True

                        

                        # もし両方のデータが更新されていたら
                        if self._current_pose_updated == True and self._target_pose_updated == True:
                                listData = [delta_time, self._gain[14], self._epsilon[14], self._current[14], self._target[14], self._output[14]]#[時間、現在値データ，目標値データ]
                                self.csvWriter.writerow(listData)
				#self._d_poseout.data = self._d_pose_target.data

                                #k = 1
                                #self._epsilon = [0]*24
                                #for n in range(24):
                                #        self._epsilon[n] = self._pose_target[n] - self._pose_position[n] #ここにエラーが出るが解決策がわからない
                                #        self._sum[n] += self.epsilon[n]
                                #        self._d_poseout.data[n] = self._d_pose_target[n] + k * self._sum[n]

                                

                        # Calculate Output Value
                        for i in range(24):
                                self._epsilon[i] = self._target[i] - self._current[i]
                                self._ringBuffer[i].push(self._epsilon[i])
                                self._sum[i] = self._ringBuffer[i].getSum()
                                self._output[i] = self._target[i] + self._gain[i]*self._sum[i]

                        self._d_poseout.data = self._output
                        self._poseoutOut.write()
                        print self._d_poseout.data
                        
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

