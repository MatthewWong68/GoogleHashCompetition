from itertools import chain
from random import sample
from pathlib import Path

def div(x, y):
  return 0 if y == 0 else x / y

def main():
  for File in Path().glob("*_*.txt"):
    photos, cv, horizontal, indices = [], [], [], {}
    with open(File) as o:
      photos = list(map(lambda s: (s[1].strip().split()[0] == "H", (s[0], set(s[1].strip().split()[2:]))), enumerate(o.readlines(), start=-1)))[1:]
      horizontal = list(map(lambda p: p[1], filter(lambda p: p[0], photos)))
      cv = list(map(lambda p: p[1], filter(lambda p: not p[0], photos)))

    # The format
    for index, tags in photos:
      # index can be a tuple of two vertical indexes
      break

    #Preprocessing of vertical images.
    cv.sort(key=lambda p: len(p[1]))
    vertical = [((cv[i][0], cv[-i][0]), cv[i][1]|cv[-i][1]) for i in range(len(cv)//2)] 
    
    #include indices of Vs
    for i, t in list(chain(horizontal, vertical)):
      for tag in t:
        if tag not in indices:
          indices[tag] = []
        indices[tag].append(i)
  

    #Find best pairs for Horizontal & pseudo-Horizontal images. ~50% overlap for best score.

    slideshow = []

    index, tags = sample(chain(horizontal, vertical), 1)[0]

    for image, image_tags in zip(index, tags):
      #1. Randomly select half of the tags from an image,
      current_tag_sample = sample(tags, len(tags)//2)
      #2. Find intersection of images with these tags
      similar_images = set().union(*[set(indices[tag]) for tag in tags])
      #3. Pick this one as next slide, remove it from indices then repeat.
      slideshow.append(similar_images.pop())

    


    



    print(f"{len(indices)} tags, {len(photos)} photos in {File.name}")
    print(f"Such as {sample(photos, 1)[0]}")
    print(f"It has {len(horizontal)} horizontal and {len(vertical)} vertical images")
    print(f"Its most unique tag is shared by {min(map(len, indices.values()))} photos")
    ic = list(sorted(map(len, indices.values())))
    lic = len(ic)
    print(f"Its median tag is shared by {ic[lic//2]} photos")
    print(f"Its 95th% tag is shared by {ic[int(lic*0.95)]} photos")
    print()

    with open(f"{File.stem}.out", "wr") as o:
      for index in slideshow:
        if type(index) == tuple or type(index) == list:
          o.write(" ".join(map(str, index)))
        else:
          o.write(str(index)) # just in case it's not a tuple
        o.write("\n")
  ...

if __name__ == "__main__":
  main()
