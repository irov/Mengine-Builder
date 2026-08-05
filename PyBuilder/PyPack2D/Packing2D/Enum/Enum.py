def cmp(a,b):
   if a < b: return -1
   if b < a: return 1
   return 0


def Enum(*names):
   ##assert names, "Empty enums are not supported" # <- Don't like empty enums? Uncomment!

   class EnumClass(object):
      __slots__ = names
      def __iter__(self):        return iter(constants)
      def __len__(self):         return len(constants)
      def __getitem__(self, i):  return constants[i]
      def __repr__(self):        return 'Enum' + str(names)
      def __str__(self):         return 'enum ' + str(constants)

   class EnumValue(object):
      __slots__ = ('__value')
      def __init__(self, value): self.__value = value
      Value = property(lambda self: self.__value)
      EnumType = property(lambda self: EnumType)
      def __hash__(self):        return hash(self.__value)
      def __cmp__(self, other):
         # C fans might want to remove the following assertion
         # to make all enums comparable by ordinal value {;))

        if hasattr(other, "EnumType") is False:
            return -1

        if self.EnumType is not other.EnumType:
            return -1

        return cmp(self.__value, other.__value)
      def __lt__(self, other):   return self.__cmp__(other) < 0
      def __eq__(self, other):   return self.__cmp__(other) == 0
      def __invert__(self):      return constants[maximum - self.__value]
      def __nonzero__(self):     return bool(self.__value)
      def __repr__(self):        return "%s = %i" % (str(names[self.__value]),self.__value )

   maximum = len(names) - 1
   constants = [None] * len(names)
   for i, each in enumerate(names):
      val = EnumValue(i)
      setattr(EnumClass, each, val)
      constants[i] = val
   constants = tuple(constants)
   EnumType = EnumClass()
   return EnumType


if __name__ == '__main__':
   print( '\n*** Enum Demo ***')
   print( '--- Days of week ---')
   Days = Enum('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su')
   print( Days)
   print( Days.Mo)
   print( Days.Fr)
   print( Days.Mo < Days.Fr)
   print( list(Days))
   for each in Days:
      print( 'Day:', each)
   print( '--- Yes/No ---')
   Confirmation = Enum('No', 'Yes')
   answer = Confirmation.No
   print( 'Your answer is not', ~answer)
