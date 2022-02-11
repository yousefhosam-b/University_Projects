// tableObjects
class tableObjects {
  PVector pos, bsize;
  tableObjects(float x, float y, float z, float b, float h, float t) {
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

class Table {
  PVector pos, bsize;
  ArrayList<tableObjects> tableObjects = new ArrayList<tableObjects>();
  Table(float x, float z, float tThickness, float h1) { //width,depth,tableThickness,legThickness,legLength

    // legs
    float w = (x > z) ? z : x;
    tableObjects.add(new tableObjects((-x/2)+w*0.1, -h1/2, z/2-w*0.1, w*0.1, h1, w*0.1));
    tableObjects.add(new tableObjects((x/2)-w*0.1, -h1/2, z/2-w*0.1, w*0.1, h1, w*0.1));
    tableObjects.add(new tableObjects((-x/2)+w*0.1, -h1/2, -z/2+w*0.1, w*0.1, h1, w*0.1));
    tableObjects.add(new tableObjects((x/2)-w*0.1, -h1/2, -z/2+w*0.1, w*0.1, h1, w*0.1));

    // surface  
    tableObjects.add(new tableObjects(0, -h1-tThickness/2, 0, x, tThickness, z));
  }

  void show() {
    for (tableObjects obj : tableObjects) 
      obj.show();
  }
}
