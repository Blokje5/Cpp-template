#include <Tmp/example.h>
#include <gtest/gtest.h>

TEST(Example, Add)
{
  EXPECT_EQ(tmp::add(2, 3), 5);
  EXPECT_EQ(tmp::add(-1, 1), 0);
  EXPECT_EQ(tmp::add(0, 0), 0);
}
