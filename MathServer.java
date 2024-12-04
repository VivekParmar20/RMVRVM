public class MathServer {

  public static void main(String[] args) {
    Thread computationThread = new Thread(() -> {
      System.out.println("Server Started");
      double result = 1.0;
      for (int i = 0; i < 767672000; i++) {
        result = Math.tan(Math.atan(i));
      }
      System.out.println("Server Ran For: " + 767672000 + " iterations");
    });

    computationThread.start();
    
    try {
      computationThread.join();  // Wait for the computation thread to finish
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
}

