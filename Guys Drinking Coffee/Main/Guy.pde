class Guy {
  PVector pos; // origin is below butt
  PShape shape;

  public float animation_time = 0;
  public float animation_delay = 2;
  float delay_counter = 0;

  PShape rau, ral;

  public Guy(float x, float z, float h1) { //width,dept,chairheight
    pos = new PVector(x, -h1, z);
    shape = createGuyShape();
  }

  void show() {
    PShape rau_ref = shape.getChild(shape.getChildIndex(rau));
    rau_ref.translate(0, 150, -10);
    rau_ref.rotateX(map(sin(animation_time - PI/2), -1, 1, 0, PI/6));
    rau_ref.translate(0, -150, 10);

    PShape ral_ref = rau_ref.getChild(rau_ref.getChildIndex(ral));
    ral_ref.translate(0, 120, -10);
    ral_ref.rotateX(map(sin(animation_time - PI/2), -1, 1, 0, PI/5));
    ral_ref.translate(0, -120, 10);

    shape(shape);

    ral_ref.translate(0, 120, -10);
    ral_ref.rotateX(-map(sin(animation_time - PI/2), -1, 1, 0, PI/5));
    ral_ref.translate(0, -120, 10);

    rau_ref.translate(0, 150, -10);
    rau_ref.rotateX(-map(sin(animation_time - PI/2), -1, 1, 0, PI/6));
    rau_ref.translate(0, -150, 10);

    animation_time += 0.01;
  }
  
 
  PShape createGuyShape() {
    PShape guy = createShape(GROUP);

    //torso
    PShape torso = createShape(BOX, 70, 100, 30);
    torso.translate(0, pos.y - 60, 10);
    guy.addChild(torso);

    //head
    PShape neck = createShape(BOX, 15, 20, 15);
    neck.translate(0, pos.y - 120, 10);
    guy.addChild(neck);
    push();
    noStroke();
    PShape head = createShape(SPHERE, 30);
    head.translate(0, pos.y - 145, 10);
    guy.addChild(head);
    pop();

    //left leg
    //upperleg
    PShape llu = createShape(BOX, 20, 20, 60);
    llu.translate(30, pos.y-20, 30);
    guy.addChild(llu);
    //lowerleg
    PShape lll = createShape(BOX, 20, 60, 20);
    lll.translate(30, pos.y+20, 50);
    guy.addChild(lll);

    //right leg
    //upperleg
    PShape rru = createShape(BOX, 20, 20, 60);
    rru.translate(-30, pos.y-20, 30);
    guy.addChild(rru);
    //lowerleg
    PShape rrl = createShape(BOX, 20, 60, 20);
    rrl.translate(-30, pos.y+20, 50);
    guy.addChild(rrl);

    //left arm
    //upperarm
    PShape lau = createShape(BOX, 20, 60, 20);
    lau.translate(45, pos.y-80, 10);
    guy.addChild(lau);
    //lowerleg
    PShape lal = createShape(BOX, 15, 15, 70);
    lal.translate(45, pos.y-45, 35);
    guy.addChild(lal);

    //right arm
    //upperarm
    rau = createShape(GROUP);
    PShape subrau = createShape(BOX, 20, 60, 20);
    subrau.translate(-45, pos.y-80, 10);
    rau.addChild(subrau);
    guy.addChild(rau);
    //lowerarm
    ral = createShape(GROUP);
    PShape subral = createShape(BOX, 15, 15, 70);
    subral.translate(-45, pos.y-45, 35);
    ral.addChild(subral);  
    rau.addChild(ral);
    
    return guy;
  }
}
