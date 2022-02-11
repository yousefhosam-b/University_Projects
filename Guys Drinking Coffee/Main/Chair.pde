// chairObjects
class chairObjects {
  PVector pos, bsize;
  chairObjects(float x, float y, float z, float b, float h, float t) {
    pos = new PVector(x, y, z);
    bsize = new PVector(b, h, t);
  }

  void show() {
    pushMatrix();
    translate(pos.x, pos.y, pos.z);
    box(bsize.x, bsize.y, bsize.z);
    popMatrix();
  }
}

class Chair {
  PVector pos, bsize;
  ArrayList<chairObjects> chairObjects = new ArrayList<chairObjects>();

  Chair(float x, float z, float cThickness, float h1, float h2) { //width,depth,chairThickness,legThickness,legLength
    // legs
    float w = (x > z) ? z : x;
    chairObjects.add(new chairObjects((-x/2)+w*0.1, -h1/2, z/2-w*0.1100, w*0.1, h1, w*0.1));
    chairObjects.add(new chairObjects((x/2)-w*0.1, -h1/2, z/2-w*0.1, w*0.1, h1, w*0.1));
    chairObjects.add(new chairObjects((-x/2)+w*0.1, -h1/2, -z/2+w*0.1, w*0.1, h1, w*0.1));
    chairObjects.add(new chairObjects((x/2)-w*0.1, -h1/2, -z/2+w*0.1, w*0.1, h1, w*0.1));

    // surface  
    chairObjects.add(new chairObjects(0, -h1-cThickness/2, 0, x, cThickness, z));

    //back
    for (float i = (-x/2)*0.8; i<=(x/2)*0.8; i+=x/5)
      chairObjects.add(new chairObjects(i, -h1-cThickness-h2/2, -z/2*0.8, w*0.05, h2, w*0.05));

    float backHeigth = h2/4;
    chairObjects.add(new chairObjects(0, -h1-cThickness-h2-backHeigth/2, -z/2*0.8, x, backHeigth, w*0.1));
  }

  void show() {
    for (chairObjects obj : chairObjects) 
      obj.show();
  }
}
