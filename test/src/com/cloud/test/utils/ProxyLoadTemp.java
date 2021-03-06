/**
 * *  Copyright (C) 2011 Citrix Systems, Inc.  All rights reserved
*
 *
 * This software is licensed under the GNU General Public License v3 or later.
 *
 * It is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

package com.cloud.test.utils;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

import org.apache.log4j.Logger;




public class ProxyLoadTemp {
	//Read data from console.input, create a console connection instance and run it for a while
	public static final Logger s_logger= Logger.getLogger(ProxyLoadTemp.class.getClass());
	public static int numThreads=0;
	public static ArrayList<ConsoleProxy> proxyList = new ArrayList<ConsoleProxy>();
	public static long begin;
	public static long end;
	public static long sum=0;
	
	public ProxyLoadTemp(){		
	}
	
	public static void main (String[] args){
		begin= System.currentTimeMillis();
		Runtime.getRuntime().addShutdownHook(new ShutdownThread(new ProxyLoadTemp()));
		ConsoleProxy.proxyIp="172-16-1-101";
		
		try 
        {
		BufferedReader consoleInput = new BufferedReader(new FileReader("console.input"));
		boolean eof = false;
		s_logger.info("Started reading file");
		while (!eof){
			String line = consoleInput.readLine();
			s_logger.info("Line is "+line);
			if (line == null){
				s_logger.info("Line "+numThreads+" is null");
                eof=true;
			}
			else{
				String[] result=null;
                try 
                {
                	s_logger.info("Starting parsing line "+line);
                   result= parseLine(line, "[,]");
                   s_logger.info("Line retrieved from the file is "+result[0]+" "+result[1]+" "+result[2]);
                   ConsoleProxy proxy = new ConsoleProxy(result[0], result[1], result[2]);
                   proxyList.add(proxy);
                   new Thread(proxy).start();
                   numThreads++;           
                   
                }
                catch (Exception ex){
                	s_logger.warn(ex);
                }
			}
			
		}
        }catch(Exception e){
        	s_logger.warn(e);
        }
		
	}
	
	public static class ShutdownThread extends Thread {
		ProxyLoadTemp temp;
		public ShutdownThread(ProxyLoadTemp temp) {
			this.temp = temp;
		}
		public void run() {
			s_logger.info("Program was running in "+numThreads+" threads");
			
			for (int j=0; j<proxyList.size(); j++){
				long av=0;
				if (proxyList.get(j).getConnectionsMade()!=0){
					av=proxyList.get(j).getResponseTime()/proxyList.get(j).getConnectionsMade();
				}
				s_logger.info("Information for "+j+" thread: Number of requests sent is "+proxyList.get(j).getConnectionsMade()+". Average response time is "+av+" milliseconds");
				sum=sum+av;

			}
			ProxyLoadTemp.end= System.currentTimeMillis();
			s_logger.info("Summary for all"+numThreads+" threads: Average response time is "+sum/numThreads+" milliseconds");
			s_logger.info("Test was running for "+(ProxyLoadTemp.end-ProxyLoadTemp.begin)/1000+" seconds");
		}
	}
	
	
	public static String[] parseLine(String line, String del) throws Exception
    {
        String del1=del.substring(1, del.length()-1);
        if (line.contains(del1)!=true)
        {
        throw new Exception();
        }
        else
        {
        String[] token = line.split(del);
        return token;  
        }

    }
	

}
