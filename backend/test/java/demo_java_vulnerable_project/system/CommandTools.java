package test.java.demo_java_vulnerable_project.system;
import jakarta.servlet.http.HttpServletRequest;

public class CommandTools {
    public void ping(HttpServletRequest request) throws Exception {
        String host = request.getParameter("host");
        new ProcessBuilder("sh", "-c", "ping " + host).start();
    }
}

package test.java.demo_java_vulnerable_project.system;

import jakarta.servlet.http.HttpServletRequest;

public class CommandTools {

    // 1. Command Injection z Runtime.exec()
    public void pingHost(HttpServletRequest request)
        throws Exception {

        String host = request.getParameter("host");

        String command = "ping -c 1 " + host;

        Runtime.getRuntime().exec(command);
    }


    // 2. Command Injection prek lupine
    public void listDirectory(HttpServletRequest request)throws Exception {

        String folder = request.getParameter("folder");

        String command = "ls " + folder;

        new ProcessBuilder("sh","-c",command).start();
       
            
            
            
    }


    // 3. Nevarna izdelava varnostne kopije
    public void backupFile(HttpServletRequest request)throws Exception {

        String filename = request.getParameter("file");

        String command ="cp " + filename + " /tmp/backup/";

        Runtime.getRuntime().exec(command);
    }


    // 4. Nevaren prikaz datoteke
    public void showFile(HttpServletRequest request)throws Exception {

        String file = request.getParameter("file");

        String command = "cat " + file;

        new ProcessBuilder("sh","-c",command).inheritIO().start();
    }


    // 5. Neposreden uporabniški vhod v ukazu
    public void directCommandExecution(HttpServletRequest request) throws Exception {

        Runtime.getRuntime().exec("ping -c 1 " + request.getParameter("host"));
    }
}