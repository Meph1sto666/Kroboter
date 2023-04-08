import os
from datetime import datetime as dt
from time import thread_time;
START:dt = dt.now();
from io import TextIOWrapper;
from types import TracebackType;
import sys;
def exHook(eType, eVal, tb:TracebackType):
	log("error", thread_time(), tb, str(eVal));
sys.excepthook = exHook;
LOG_HISTORY:int = 32;

INITIALIZED = False;
ENCRYPTED:bool = False;
LOG_FOLDER:str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/logs/";
LOGFILE:TextIOWrapper = None;

INFO:str = "info";
DEBUG:str = "debug";
WARNING:str = "warning";
ERROR:str = "error";
CRITICAL:str = "critical";
FATAL:str = "fatal";

def init():
	"""initializes the logger.
	"""
	if INITIALIZED: return
	updateConfig(True);
	INITIALIZED = True;

def padStart(s:str, t:int, c:str=" ") -> str:
	"""Filling string with characters starting from the start.

	Args:
		s (str): String to beautify.
		t (int): position to fill to.
		c (str, optional): Fill character. Defaults to " ".

	Returns:
		str: Padded string
	"""
	if len(c) > 1: c = c[0];
	f=t-len(s);
	if f < 0: f = 0;
	for i in range(f): s = c + s;
	return s;
def padEnd(s:str, t:int, c:str=" ") -> str:
	"""Filling string with characters starting from the end.

	Args:
		s (str): String to beautify.
		t (int): position to fill to.
		c (str, optional): Fill character. Defaults to " ".

	Returns:
		str: Padded string
	"""
	if len(c) > 1: c = c[0];
	f=t-len(s);
	if f < 0: f = 0;
	for i in range(f): s += c;
	return s;
def formatTime(s:float) -> str:
	"""Makes timestamps more readable

	Args:
		s (float): Time in seconds

	Returns:
		str: Beautified string
	"""
	sp = str(s).split(".");
	return padStart(sp[0], 9) + "." + sp[1].zfill(6);

def getCLogfilePath() -> str:
	"""Returns the current logfile path

	Returns:
		str: path
	"""
	return LOG_FOLDER + dt.strftime(dt.now(), "%Y%m%d") + ".log";

def updateConfig(forceUpdate:bool=False):
	global LOGFILE;
	path = getCLogfilePath();
	if rollover() or forceUpdate:
		if not os.path.exists(path):
			os.makedirs(os.path.dirname(path), exist_ok=True);
		LOGFILE = open(path, "a", encoding="utf-8");
		clearLogHistory();

def log(level:str, threadTime:float, tb:TracebackType=None, msg:str="") -> None:
	"""Log to file

	Args:
		level (str): log level eg. info, error.
		threadTime (float): Time the process took. (get with time.thread_time())
		tb (TracebackType, optional): traceback for debugging. Defaults to None.
		msg (str, optional): message to print (mostly for INFO level). Defaults to "".
	"""
	updateConfig();
	trace:list = [];
	while tb:
		trace.append(tb);
		tb = tb.tb_next;
	for i in range(len(trace)):
		if i != len(trace) - 1: cLevel = "trace";
		else: cLevel = level;
		t:TracebackType = trace[i];
		logEntry:str = dt.now().isoformat();
		logEntry += f" ⅀:[{formatTime((dt.now() - START).total_seconds())}]";
		logEntry += f" Δ:[{formatTime(threadTime)}]";
		logEntry += f" {padEnd(cLevel.upper(), 8, '.')}:";
		logEntry += f" #{padStart(str(i), len(str(len(trace)-1)))} >{t.tb_lineno}";
		logEntry += f" {t.tb_frame.f_code.co_filename.split(os.sep)[-1].removesuffix('.py')}";
		logEntry += f".{t.tb_frame.f_code.co_name} :";
		if i == len(trace) - 1: logEntry += " " + msg + "\n";
		else: logEntry += "\n";
		maxLen = len(sorted(t.tb_frame.f_locals.items(), key=lambda l:len(l[0]), reverse=True));
		if i != 0:
			for (k,v) in t.tb_frame.f_locals.items(): logEntry += f"\t{padEnd(k, maxLen+1, '.')}: {v}\n";
		LOGFILE.write(logEntry);
	if tb == None:
		logEntry:str = dt.now().isoformat();
		logEntry += f" ⅀:[{formatTime((dt.now() - START).total_seconds())}]";
		logEntry += f" Δ:[{formatTime(threadTime)}]";
		logEntry += f" {padEnd(level.upper(), 8, '.')}:";
		logEntry += " " + msg + "\n";
		LOGFILE.write(logEntry);
	LOGFILE.flush();
	os.fsync(LOGFILE.fileno());
	
def end() -> None:
	"""Ends logging
	"""
	LOGFILE.close();
	  
def rollover() -> bool:
	"""Checks if a new logfile should be created

	Returns:
		bool: _description_
	"""
	if LOGFILE == None: return True;
	# return LOGFILE.name.split(".")[-2][-14:-6] != dt.strftime(dt.now(), "%Y%m%d");
	return LOGFILE.name.split(".")[-2][-8:] != dt.strftime(dt.now(), "%Y%m%d");


def clearLogHistory() -> None:
	"""Reduces saved logfiles to the amount of LOG_HISTORY.
	"""
	logHistory:list = os.listdir(LOG_FOLDER);
	logHistory.sort(reverse=True);
	for log in logHistory[LOG_HISTORY:]: os.remove(LOG_FOLDER + log);