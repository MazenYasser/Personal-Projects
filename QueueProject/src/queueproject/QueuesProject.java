/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package queueproject;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;

/**
 *
 * @author mazen
 */
public class QueuesProject {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws ScriptException {
       QueueFrame frame= new QueueFrame();
       frame.setTitle("Queue problem solver");
       frame.setVisible(true);
       
       ScriptEngineManager arithmetic = new ScriptEngineManager();
       ScriptEngine arithmetic_engine = arithmetic.getEngineByName("JavaScript");
       double x = Double.valueOf(String.valueOf(arithmetic_engine.eval("1+2-1")));
    }
    
}
