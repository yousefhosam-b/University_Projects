class Chat {
  Slide<Page> Chat = new Slide();
  int current = 0;

  public Chat() {
    initializeChats();
  }

  void initializeChats() {
    Chat.add(new EmresChat("Emre:\nThank you for accepting my invitation and coming to the garden", #FBFF00));
    Chat.add(new MehmetsChat("Mehmet:\nTabiiki bro you told me there is urgent thing", #82F2E4));
    Chat.add(new EmresChat("Emre:\nYes, Mehmet abi can I ask you something please", #FBFF00));
    Chat.add(new MehmetsChat("Mehmet:\nOf course dostum anything you want", #82F2E4));
    Chat.add(new EmresChat("Emre:\nI was trying to do the homework that our teacher gave to us", #FBFF00));
    Chat.add(new MehmetsChat("Mehmet:\nVery nice, and how could you solve it?", #82F2E4));
    Chat.add(new EmresChat("Emre:\nNooo, that's why I asked you to come, I need to know how did you solve it", #FBFF00));
    Chat.add(new MehmetsChat("Mehmet:\nWell, I found online book from BAU library, I understood the topic better while reading it", #82F2E4));
    Chat.add(new EmresChat("Emre:\nHow can I use BAU library, I can't go to the campus, I want to read online too", #FBFF00));
    Chat.add(new MehmetsChat("Mehmet:\nIt's very simple Emre, I will show you once we get inside", #82F2E4));
    Chat.add(new EmresChat("Emre:\nThank you a lot bro, I owe you one", #FBFF00));
    Chat.add(new MehmetsChat("Mehmet:\nNah you don't owe me anything, coming to the garden was enough", #82F2E4));
    Chat.add(new EmresChat("Emre:\nAhahaahaha thanks bro I've made a lot of changes since your last visit", #FBFF00));
    Chat.add(new MehmetsChat("Mehmet:\nYea I can see that, nice work", #82F2E4));
  }

  void draw() {
    Chat.get(current).draw();
  }

  class Slide<T> {
    private ArrayList<T> slides;
    public Slide() {
      slides = new ArrayList();
    }
    public void add(T t) {
      slides.add(t);
    }
    public int size() {
      return slides.size();
    }
    public T get(int index) {
      return slides.get(index);
    }
  }

  abstract class Page {
    protected int a, b;
    private Page(int a) {
      this.a = a;
    }
    abstract void draw();
  }

  class EmresChat extends Page {
    private String text;
    public EmresChat(String text, int a) {
      super(a);
      this.text = text;
    }

    void draw() {
      noStroke();

      fill(a);
      rect(-130, 100, 450, 200);

      textSize(24);
      fill(0);
      text(text, -100, 120, 400, 200);
    }
  }

  class MehmetsChat extends Page {
    private String text;
    public MehmetsChat(String text, int a) {
      super(a);
      this.text = text;
    }

    void draw() {
      noStroke();

      fill(a);
      rect(330, 100, 450, 200);

      textSize(24);
      fill(0);
      text(text, 360, 120, 400, 200);
    }
  }
}
